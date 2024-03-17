  
from ._table_autoloader import AutoloaderTable

PROJECT = "contoso_retail_dw"
# register tables here and map them to a table Class
# if adding new properties then they must be added
# to the __init__ of the ._base_table.BaseTable
def tables():

  return {
    "dim_account": {
      "project": PROJECT,
      "filename": "dim_account",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_channel": {
      "project": PROJECT,
      "filename": "dim_channel",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_account": {
      "project": PROJECT,
      "filename": "dim_account",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_channel": {
      "project": PROJECT,
      "filename": "dim_channel",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_currency": {
      "project": PROJECT,
      "filename": "dim_currency",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_customer": {
      "project": PROJECT,
      "filename": "dim_customer",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_date": {
      "project": PROJECT,
      "filename": "dim_date",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_employee": {
      "project": PROJECT,
      "filename": "dim_employee",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_entity": {
      "project": PROJECT,
      "filename": "dim_entity",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_geography": {
      "project": PROJECT,
      "filename": "dim_geography",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_machine": {
      "project": PROJECT,
      "filename": "dim_machine",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_outage": {
      "project": PROJECT,
      "filename": "dim_outage",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_product": {
      "project": PROJECT,
      "filename": "dim_product",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_product_category": {
      "project": PROJECT,
      "filename": "dim_product_category",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_product_sub_category": {
      "project": PROJECT,
      "filename": "dim_product_sub_category",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_promotion": {
      "project": PROJECT,
      "filename": "dim_promotion",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_sales_territory": {
      "project": PROJECT,
      "filename": "dim_sales_territory",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_scenario": {
      "project": PROJECT,
      "filename": "dim_scenario",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "dim_store": {
      "project": PROJECT,
      "filename": "dim_store",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "fact_exchange_rate": {
      "project": PROJECT,
      "filename": "fact_exchange_rate",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "fact_inventory": {
      "project": PROJECT,
      "filename": "fact_inventory",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "fact_it_machine": {
      "project": PROJECT,
      "filename": "fact_it_machine",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "fact_it_sla": {
      "project": PROJECT,
      "filename": "fact_it_sla",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "fact_online_sales": {
      "project": PROJECT,
      "filename": "fact_online_sales",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "fact_sales": {
      "project": PROJECT,
      "filename": "fact_sales",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "fact_sales_quota": {
      "project": PROJECT,
      "filename": "fact_sales_quota",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    },
    "fact_strategy_plan": {
      "project": PROJECT,
      "filename": "fact_strategy_plan",
      "default": AutoloaderTable,
      "primary_keys": [
      ]
    }
  }