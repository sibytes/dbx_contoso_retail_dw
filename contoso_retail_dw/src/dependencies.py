# Databricks notebook source
# MAGIC %sql
# MAGIC use catalog system;
# MAGIC use schema information_schema;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from dev_hub.stage_contoso_retail_dw.production_product_review where `_corrupt_record` is not null
