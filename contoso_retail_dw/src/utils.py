# Databricks notebook source
# MAGIC %md
# MAGIC # Main Entry Point for a Table Load Task
# MAGIC
# MAGIC This default notebook is executed using Databricks Workflows as defined in resources/ingest_contoso_retail_dw_job.yml.

# COMMAND ----------

# MAGIC %pip install pyyaml
# MAGIC

# COMMAND ----------

from etl import tables

dependencies_list = [f"            - task_key: {table}" for table, details in tables().items()]

with open("./scratch.txt", "w") as f:
  f.write("\n".join(dependencies_list))



# COMMAND ----------

from etl import tables
import yaml

task = {
  "task_key": "",
  "depends_on": [
  ],
  "notebook_task" : None,
  "existing_cluster_id": "0317-110841-x2mt4zty"
}
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

tasks = []
prev_table = "initialise"
i = 0
for table, details in tables().items():
  this_task = task.copy()
  this_task["task_key"] = table
  this_task["depends_on"] = [{"task_key": prev_table}]
  this_task["notebook_task"] = {
    "notebook_path": "/Repos/shaun.ryan@shaunchiburihotmail.onmicrosoft.com/dbx_contoso_retail_dw/contoso_retail_dw/src/load_table",
    "base_parameters": {
      "table": table
    },
    "source": "WORKSPACE"
  }
  tasks.append(this_task)

  if i == 16:
    prev_table = "initialise"
    i = 0
  else:
    prev_table = table
    i += 1


tasks = {"tasks": tasks}

with open("../scratch/scratch.yaml", "w") as f:
  f.write(yaml.dump(tasks, indent=4, Dumper=NoAliasDumper))


# COMMAND ----------


checkpoints = {p.path: dbutils.fs.rm(p.path, True) for p in dbutils.fs.ls("/Volumes/dev_hub/checkpoints/contoso_retail_dw")}
checkpoints

# COMMAND ----------


# from etl.utils import convert_schema, FileTypes

# convert_schema("../schema/")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from dev_hub.contoso_retail_dw.`_audit`

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from dev_hub.stage_contoso_retail_dw.sales_currency_rate

# COMMAND ----------

from etl import tables, PROJECT
import json
import yaml

format = "csv"
ext = "csv"
filename_mask = f"{table}-*"
env = "dev"
options = {"sep": "|", "header": True, "inferSchema": True}
root = f"/Volumes/{env}_landing/{PROJECT}/{PROJECT}/{format}"

for table, details in tables().items():
  path = f"{root}/{table}/*/{filename_mask}.{ext}"

  df = spark.read.format("csv").options(**options).load(path)
  schema = json.loads(df.schema.json())
  with open(f"../schema/{table}.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(schema, indent=4))

  with open(f"../schema/{table}.yaml", "w", encoding="utf-8") as f:
    f.write(yaml.safe_dump(schema, indent=4))

