from pyspark.sql import DataFrame, functions as fn
from datetime import datetime
from typing import Optional
from ._base_table import BaseTable
from pyspark.sql.streaming import StreamingQuery
from databricks.sdk.runtime import dbutils
from ._base_table import BaseTable



class AutoloaderTable(BaseTable):

  def __init__(
      self,**kwargs
  ):
    super().__init__(**kwargs)
    self.source_options = {
      "cloudFiles.format": "csv",
      "cloudFiles.schemaLocation": self.checkpoint_path,
      "cloudFiles.useIncrementalListing": "auto",
      # schema
      "inferSchema": "false",
      "mode": "true",
      "columnNameOfCorruptRecord": "_corrupt_record",
      # csv
      "header": "true",
      "mode": "PERMISSIVE",
      "encoding": "utf-8",
      "delimiter": "|",
      "escape": '"',
      "nullValue": "",
      "quote": '"',
      "emptyValue": ""
    }

  def stage_into(
      self, 
      process_id:int, 
      merge_schema=True, 
      force=False,
      modified_after:Optional[datetime] = None,
      modified_before:Optional[datetime] = None,
  ):
    

    self._create_stage_table()

    modifieds = {}
    if isinstance(modified_after, datetime):
      fmt_modified_after = modified_after.strftime("%Y-%m-%d %H:%M:%S")
      modifieds["modifiedAfter"] = fmt_modified_after
    elif modified_after is not None:
      raise Exception(f"Invalid modified_after={modified_after} of type={type(modified_after)}. Parameter must be a datetime or None")

    if isinstance(modified_before, datetime):
      fmt_modified_before = modified_before.strftime("%Y-%m-%d %H:%M:%S")
      modifieds["modifiedBefore"] = fmt_modified_before
    elif modified_before is not None:
      raise Exception(f"Invalid modified_before={modified_before} of type={type(modified_before)}. Parameter must be a datetime or None")

    if modifieds:
      self._logger.info(f"modified is set to filter on {modifieds}")
      self.source_options = self.source_options | modifieds
    else:
      self._logger.info("modified is None and therefore not set")

    if force:
      self._logger.info(f"clearing checkpoints at {self.checkpoint_path} data will be fully reloaded.")
      dbutils.fs.rm(self.checkpoint_path, True)
    
    self._logger.info(f"autoload {self.source_path} into `{self.stage_db}`.`{self.name}` with merge_schema = {str(force).lower()} and force = {str(force).lower()}")

    destination_options = {
      "mergeSchema": merge_schema,
      "checkpointLocation": self.checkpoint_path
    }
    stream_data: StreamingQuery = (
      self.spark.readStream
        .schema(self.schema)
        .format("cloudfiles")
        .options(**self.source_options)
        .load(self.source_path)
        .selectExpr(
          *self._get_select(self.schema),
          """
            to_date(substring_index(substring_index(
              `_metadata`.file_name,
            "-", -1), ".", 1), "yyyyMMdd")
            as _snapshot_date
          """,
          f"cast({process_id} as bigint) as _process_id",
          "now() as _load_date",
          "_metadata"
        )
        .writeStream
        .options(**destination_options)
        .trigger(availableNow=True)
        .toTable(f"`{self.stage_db}`.`{self.name}`")
    )
    stream_data.awaitTermination()
    

  def load_audit(
    self, 
    process_id: int
  ):

    sql = f"""
      select
          '{self.name}' as `table`,            
          count(1) as total_count,
          sum(if(_corrupt_record is null, 1, 0)) as valid_count,  
          sum(if(_corrupt_record is not null, 1, 0)) as invalid_count,
          valid_count / total_count as invalid_ratio,         
          _metadata.file_path,              
          _metadata.file_name,              
          _metadata.file_size, 
          _metadata.file_modification_time,             
          _metadata.file_block_start,       
          _metadata.file_block_length,
          if(invalid_count=0, true, false) as schema_valid,   
          _snapshot_date as snapshot_date,                     
          _process_id as process_id,
          now() as stage_load_date,
          cast(null as timestamp) as hub_load_date         
      from {self.stage_db}.{self.name}
      where _process_id = {process_id}
      group by            
          file_path,              
          file_name,              
          file_size, 
          file_modification_time,             
          file_block_start,       
          file_block_length,  
          snapshot_date,                     
          process_id  
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
      and a.table = '{self.name}'
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
      schema_valid_clause = f"and a.schema_valid"

    df = self.spark.sql(f"""
      select 
        src.* except (_corrupt_record, _load_date, _process_id, _metadata, _snapshot_date),
        src._snapshot_date,
        src._process_id,
        now() as _load_date,
        src._metadata.file_name as _file_name,
        false as _is_migration,
        true _is_current,
        src._snapshot_date as _from_date,
        to_date('9999-12-31') as _to_date
      from {self.stage_db}.{self.name} src
      join {self.db}._audit a 
        on src._metadata.file_name = a.file_name
       and src._metadata.file_size = a.file_size
       and src._metadata.file_modification_time = a.file_modification_time
      where src._process_id = {process_id}
        {schema_valid_clause}
        and src._corrupt_record is null
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








