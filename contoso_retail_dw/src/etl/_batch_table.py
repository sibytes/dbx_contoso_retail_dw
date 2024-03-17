import logging
import os
import json
from pyspark.sql.types import StructType
from pyspark.sql import SparkSession, DataFrame
from datetime import datetime
from typing import Optional
from ._base_table import BaseTable
from .utils import Variables


class BatchTable(BaseTable):

  def __init__(
      self,**kwargs
  ):
    super().__init__(**kwargs)

    # load spark and sql
    self.schema:StructType = self._load_schema(name = self.name)
    self.schema_ddl:str = ",\n".join(self._get_ddl(self.schema, header=True))

    self.sql_stage_table = self._load_sql(
      name = f"stage/{self.stage_db}.table",
      variables = {
        Variables.DATABASE: self.stage_db,
        Variables.TABLE: self.name
      }
    )

    self.sql_table = self._load_sql(
      name = f"base/{self.db}.table",
      variables = {
        Variables.DATABASE: self.db,
        Variables.TABLE: self.name,
        Variables.COLUMNS: self.schema_ddl
      }
    )


  def stage_into(
      self, 
      process_id:int, 
      merge_schema=True, 
      force=False,
      modified_after:Optional[datetime] = None,
      modified_before:Optional[datetime] = None,
  ):
    self._logger.info(f"creating stage table `{self.stage_db}`.`{self.name}`")
    sql = f"""
      create schema if not exists `{self.stage_db}`
    """
    self._logger.debug(sql)
    self.spark.sql(sql)

    self._logger.debug(self.sql_stage_table)
    self.spark.sql(self.sql_stage_table)

    modifieds = []
    if isinstance(modified_after, datetime):
      fmt_modified_after = modified_after.strftime("%Y-%m-%d %H:%M:%S")
      modifieds.append(f"'modifiedAfter' = '{fmt_modified_after}'")
    elif modified_after is not None:
      raise Exception(f"Invalid modified_after={modified_after} of type={type(modified_after)}. Parameter must be a datetime or None")

    if isinstance(modified_before, datetime):
      fmt_modified_before = modified_before.strftime("%Y-%m-%d %H:%M:%S")
      modifieds.append(f"'modifiedBefore' = '{fmt_modified_before}'")
    elif modified_before is not None:
      raise Exception(f"Invalid modified_before={modified_before} of type={type(modified_before)}. Parameter must be a datetime or None")

    if modifieds:
      modified_clause = ",".join(modifieds)
      self._logger.info(f"modified_after is set to filter on {modified_clause}")
    else:
      modified_clause = ''
      self._logger.info("modified_after is None and therefore not set")

    
    self._logger.info(f"copy into {self.source_path} into `{self.stage_db}`.`{self.name}` with merge_schema = {str(force).lower()} and force = {str(force).lower()}")
    sql = f"""
      copy into `{self.stage_db}`.`{self.name}`
      FROM
      (
          select
            cast({process_id} as bigint) as process_id,
            now() as load_date,
            _metadata as metadata,
            from_csv(
              _c0, 
              '{self.schema_ddl}',
              map('mode', 'PERMISSIVE')
            ) as data
          FROM '{self.source_path}'
      )
      FILEFORMAT = CSV
      FORMAT_OPTIONS (
        {modified_clause}
        'mergeSchema' = 'true',
        'delimiter' = '~',
        'header' = 'false'
      )
      COPY_OPTIONS (
        'force' = '{str(force).lower()}',
        'mergeSchema' = '{str(merge_schema).lower()}'
      );
    """
    self._logger.debug(sql)
    self.spark.sql(sql)
    

  def load_audit(
    self, 
    process_id: int
  ):

    sql = f"""
      select
          {self.name} as `table`,            
          count(1) as total_count,
          sum(if(data._corrupt_record is null, 1, 0)) as valid_count,  
          sum(if(data._corrupt_record is not null, 1, 0)) as invalid_count,
          valid_count / total_count as invalid_ratio         
          _metadata.file_path,              
          _metadata.file_name,              
          _metadata.file_size, 
          _metadata.file_modification_time,             
          _metadata.file_block_start,       
          _metadata.file_block_length,      
          if(invalid_count=0, true, false) as schema_valid,                        
          h.process_id,
          now() as load_date         
      from {self.stage_db}.{self.name}
      where h.process_id = {process_id}
      group by all
    """
    self._logger.debug(sql)
    
    # we have to lookup what's loaded 1st
    # we cannot merge append only because of concurrency control.
    df = self.spark.sql(sql)
    df.createOrReplaceTempView(f"audit_{self.name}")
    count_loading = df.count()
    count_loaded = self.spark.sql(f"""
      select 1 cnt 
      from {self.db}._audit a
      where a.process_id = {process_id}
    """).count()
    df_audit = None
    self._logger.info(f"_audit logging count_loaded={count_loaded} and count_loading={count_loading}")
    if count_loaded == 0 and count_loading > 0:
      self._logger.info(f"loading {count_loading} records into _audit")
      df_audit = df.write.format("delta").mode("append").saveAsTable(f"{self.db}._audit")
    elif count_loaded == count_loading:
      self._logger.info(f"{count_loaded} records already logger into _audit")
    else:
      raise Exception(f"Inconistency has occured in the _audit logging count_loaded={count_loaded} and count_loading={count_loading}")

    return df_audit


  def extract(
    self,
    process_id:int,
    hold_file_if_schema_failed:bool = True
  ):
    self._logger.info(f"extracting {self.name}")
    schema_valid_clause = ""
    if hold_file_if_schema_failed:
      schema_valid_clause = f"and hf.schema_valid"

    df = self.spark.sql(f"""
      select 
        src.data.* except (_corrupt_record),
        src._metadata.file_name as _file_name,
        to_timestamp(substring_index(substring_index(src._metadata.file_name,'-', -1), '.', 1), 'yyyyMMddHHmmss') as _snapshot_date,
        now() as _load_date,
        src.process_id as _process_id,
        false as _is_migration
      from {self.stage_db}.{self.name} src
      join {self.db}._audit a 
        on src._metadata.file_name = a.file_name
       and src._metadata.file_size = a.file_size
       and src._metadata.file_modification_time = a.file_modification_time
      where src._process_id = {process_id}
        {schema_valid_clause}
        and src.data._corrupt_record is null
    """)
    
    return df

  def transform(self, df:DataFrame):
    self._logger.info(f"transforming {self.name}")
    return df

  def load(
    self,
    df:DataFrame
  ):
    self._logger.info(f"loading {self.name}")
    self._logger.debug(self.sql_table)
    df_audit = self.spark.sql(self.sql_table)
    initial_load:bool = False
    df.createOrReplaceTempView(f"src_{self.name}")

    try:
      df_check = self.spark.sql(f"select * from {self.db}.{self.name} limit 1")
      df_check.collect()
    except Exception:
      initial_load = True
  
    if initial_load:
      # this is handy to do if on the 1st load your reverse engineering your
      # sql create table since you can't merge unless the table already has a schema in place
      self._logger.info("initial load - loading into table using saveAsTable")
      df = (df.write
            .format("delta")
            .option("mergeSchema", True)
            .mode("append")
            .saveAsTable(f"{self.db}.{self.name}")
      )
    else:
      self._logger.info("loading into table using merge")
      self.spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", True)
      on_clause = self._get_merge_on_clause()
      sql = (f"""
        merge into {self.db}.{self.name} dst
        using src_{self.name} src
        on {on_clause}
        when not matched then insert *
      """)
      self._logger.debug(sql)
      df_audit = self.spark.sql(sql)

    return df_audit








