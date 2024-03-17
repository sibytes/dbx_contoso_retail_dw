import os
import logging
from pyspark.sql import SparkSession
from enum import Enum
import jinja2
from typing import Dict
import yaml
import json

class Variables(Enum):
    DATABASE = "database"
    TABLE = "table"
    PROJECT = "project"
    CATALOG = "catalog"
    COLUMNS = "columns"

class Environments(Enum):
  dev = "adb-8723178682651460"
  tst = "N/A"
  pre = "N/A"
  prd = "N/A"

class FileTypes(Enum):
  yaml = ".yaml"
  yml = ".yml"
  json = ".json"

  def __str__(self):
    return self.value

def render_jinja(
  data: str, 
  replacements:Dict[Variables, str]
):
  logger = logging.getLogger(__name__)
  logger.debug(f"Rendering Jinja string {data}")
  if data and isinstance(data, str):
      replace = {k.value: v for (k, v) in replacements.items()}
      skip = False
      for k, v in replace.items():
          if v is None and "{{" + k + "}}" in data.replace(" ", ""):
              skip = True
              break

      if not skip:
          template: jinja2.Template = jinja2.Template(data)
          data = template.render(replace)
  logger.debug(f"Rendered Jinja string {data}")

  return data
  
def load_sql(
  name:str, 
  root:str="./../sql", 
  variables: Dict[Variables, str] | None = None
):
  logger = logging.getLogger(__name__)
  path = os.path.join(os.getcwd(), root, f"{name}.sql")
  logger.info(f"loading sql {path}")

  with open(path, "r", encoding="utf-8") as f:
    sql = f.read()

  if isinstance(variables, dict):
    sql = render_jinja(sql, variables)
  
  return sql

def get_environment(spark:SparkSession):

  logger = logging.getLogger(__name__)

  workspace = spark.conf.get("spark.databricks.workspaceUrl").split(".")[0]
  logger.debug(f"Detected the workspace {workspace} for environment configuration")
  try:
    env = Environments(workspace)
  except Exception as e:
    msg = f"Workspace {workspace} not found in Environments enum"
    logger.error(msg)
    raise Exception(msg)
  
  logger.info(f"Detected the {env} environment")

  return env

def convert_schema(directory:str):
  logger = logging.getLogger(__name__)
  encoding = "utf-8"
  for filename in os.listdir(directory):
    path, ext = os.path.splitext(filename)
    full_path = os.path.abspath(os.path.join(directory, filename))
    

    if  FileTypes(ext) in (FileTypes.yml,FileTypes.yaml):
      with open(full_path, "r", encoding=encoding) as f:
        data = yaml.safe_load(f)

      path, ext = os.path.splitext(full_path)
      to_full_path = f"{path}{str(FileTypes.json)}"
      logger.info(f"converting {full_path} to {to_full_path}")
      with open(to_full_path, "w", encoding=encoding) as f:
        f.write(json.dumps(data, indent=4))

    elif FileTypes(ext) == FileTypes.json:
      with open(full_path, "r", encoding=encoding) as f:
        data = json.load(f)

      path, ext = os.path.splitext(full_path)
      to_full_path = f"{path}{str(FileTypes.yaml)}"
      logger.info(f"converting {full_path} to {to_full_path}")
      with open(to_full_path, "w", encoding=encoding) as f:
        f.write(yaml.safe_dump(data, indent=4))

    else:
        continue



  
