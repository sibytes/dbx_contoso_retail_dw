import logging
from .table_config import tables
from pyspark.sql import SparkSession

def get_table(
    spark: SparkSession,
    table: str, 
    load_type: str,
    schema_version: str|None = None
  ):

  try:
    table_metadata = tables()[table]
  except KeyError as e:
    msg = f"table {table} not found in factory metadata"
    raise Exception(msg) from e
  
  try:
    table_cls = table_metadata[load_type]
    del table_metadata[load_type]
    table_metadata["name"] = table

  except KeyError as e:
    msg = f"table {table} has no class defined in the factory metadata it must have one."
    raise Exception(msg) from e

  return table_cls(spark = spark, schema_version=schema_version, **table_metadata)



