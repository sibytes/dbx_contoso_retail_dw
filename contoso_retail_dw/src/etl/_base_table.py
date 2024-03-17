from abc import ABC, abstractmethod
from pyspark.sql import DataFrame, SparkSession
import logging
from typing import Optional
from datetime import datetime
from .utils import load_sql, get_environment, FileTypes, Variables
from pyspark.sql.types import StructType
from typing import Dict
import os
import yaml
import json
import re

class BaseTable(ABC):

  _SCHEMA_PATH = "./../schema"
  _SCHEMA_FORMAT = FileTypes.yaml
  _SQL_PATH = "./../sql"
  _SRC_CATALOG = "landing"
  _DST_CATALOG = "hub"
  _VOLUME_ROOT = "Volumes"
  _STAGE_DB_PREFIX = "stage"
  
  def __init__(
      self,
      spark:SparkSession,
      schema_version:str|None,
      project:str,
      name:str,
      filename:str,
      primary_keys:list
      ):
    self._logger = logging.getLogger(self.__class__.__name__)

    self.spark = spark
    self.project = project
    self.name = name
    self.filename = filename
    self.primary_keys = primary_keys
    self.environment = get_environment(spark = self.spark).name
    self.db = project
    self.stage_db = f"{self._STAGE_DB_PREFIX}_{project}"
    self.extension = "csv"
    self.schema_version = schema_version
    root = f"/{self._VOLUME_ROOT}/{self.environment}_"
    self.source_path = f"{root}{self._SRC_CATALOG}/{self.project}/{self.project}/{self.filename}/*/{self.filename}-*.{self.extension}"
    self.checkpoint_path = f"{root}{self._DST_CATALOG}/checkpoints/{self.db}/{self.stage_db}_{self.name}"
    if self.filename is not None:
      self.schema:StructType = self._load_schema(name = self.name)
      self.schema_ddl:str = ",\n".join(self._get_ddl(self.schema, header=True))
      
    self.sql_stage_table = self._load_sql(
      name = f"{self._STAGE_DB_PREFIX}/{self.stage_db}.table",
      variables = {
        Variables.DATABASE: self.stage_db,
        Variables.TABLE: self.name
      }
    )

    self.sql_table = self._load_sql(
      name = f"{self._DST_CATALOG}/{self.db}.table",
      variables = {
        Variables.DATABASE: self.db,
        Variables.TABLE: self.name,
        Variables.COLUMNS: self.schema_ddl
      }
    )

  def _create_stage_table(self):
    self._logger.info(f"Creating {self._STAGE_DB_PREFIX} table `{self.stage_db}`.`{self.name}`")
    sql = f"""
      create schema if not exists `{self.stage_db}`
    """
    self._logger.debug(sql)
    self.spark.sql(sql)

    self._logger.debug(self.sql_stage_table)
    self.spark.sql(self.sql_stage_table)

  def _get_merge_on_clause(
    self, 
    source_alias:str = "src", 
    destination_alias:str = "dst"
  ):
    sql = [ f"{source_alias}.{k} = {destination_alias}.{k}" 
           for k in self.primary_keys]
    sql = " and ".join(sql)
    return sql

  def _load_sql(
    self, 
    name:str, 
    variables: Dict[Variables, str] | None = None
  ):
    sql = load_sql(name, self._SQL_PATH, variables=variables)    
    return sql
  
  @abstractmethod
  def stage_into(
      self, 
      process_id:int, 
      merge_schema=True, 
      force=False,
      modified_after:Optional[datetime] = None,
      modified_before:Optional[datetime] = None
  ):
    pass

  @abstractmethod
  def load_audit(
    self, 
    process_id: int
  ) -> Optional[DataFrame]:
    pass

  @abstractmethod
  def extract(
    self,
    process_id:int,
    hold_file_if_schema_failed:bool = True
  ) -> DataFrame:
    pass

  @abstractmethod
  def transform(
    self, 
    df:DataFrame
  ) -> DataFrame:
    pass

  @abstractmethod
  def load(
    self,
    df:DataFrame
  ) -> DataFrame:
    pass

  def _camel_to_snake(self, name:str):
      snake = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
      return re.sub('([a-z0-9])([A-Z])', r'\1_\2', snake).lower()

  def _load_schema(self, name:str):
    
    path = os.path.join(
      os.getcwd(), 
      self._SCHEMA_PATH, 
      f"{name}.{self._SCHEMA_FORMAT.name}")
    
    self._logger.info(f"loading schema {path}")

    with open(path, "r", encoding="utf-8") as f:
      if self._SCHEMA_FORMAT in [FileTypes.yaml, FileTypes.yml]:
        data = yaml.safe_load(f)
      elif self._SCHEMA_FORMAT == FileTypes.json:
        data = json.load(f)
      else:
        # can never happen unless the pattern is broken
        raise Exception(f"Unsupported schema file type {self._SCHEMA_FORMAT}")
    
    try:
      schema = StructType.fromJson(data)
    except Exception as e:
      msg = f"failed to convert the schema defined at {path} to a spark schema. Check that is't a valid spark schema."
      self._logger.error(msg)
      raise Exception(msg) from e

    return schema
  
  def _get_ddl(self, spark_schema: StructType, header: bool = True):
    self._logger.debug(f"Converting spark schema to ddl with header={str(header)}")
    if header:
        ddl = [f"{self._camel_to_snake(f.name)} {f.dataType.simpleString()}" for f in spark_schema.fields]
        self._logger.debug(ddl)
    else:
        ddl = [
            f"_c{i} {f.dataType.simpleString()}"
            for i, f in enumerate(spark_schema.fields)
        ]
        self._logger.debug(ddl)

    return ddl
  
  def _get_select(self, spark_schema: StructType):

    select = [f"`{f.name}` as `{self._camel_to_snake(f.name)}`" for f in spark_schema.fields]
    # select = ",".join(select)
    self._logger.debug(select)
    
    return select