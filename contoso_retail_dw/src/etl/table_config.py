  
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
        "account_key"
      ]
    },
    "dim_channel": {
      "project": PROJECT,
      "filename": "dim_channel",
      "default": AutoloaderTable,
      "primary_keys": [
        "channel_key"
      ]
    },
    "dim_currency": {
      "project": PROJECT,
      "filename": "dim_currency",
      "default": AutoloaderTable,
      "primary_keys": [
        "currency_key"
      ]
    },
    "dim_customer": {
      "project": PROJECT,
      "filename": "dim_customer",
      "default": AutoloaderTable,
      "primary_keys": [
        "customer_key"
      ]
    },
    "dim_date": {
      "project": PROJECT,
      "filename": "dim_date",
      "default": AutoloaderTable,
      "primary_keys": [
        "date_key"
      ]
    },
    "dim_employee": {
      "project": PROJECT,
      "filename": "dim_employee",
      "default": AutoloaderTable,
      "primary_keys": [
        "employee_key"
      ]
    },
    "dim_entity": {
      "project": PROJECT,
      "filename": "dim_entity",
      "default": AutoloaderTable,
      "primary_keys": [
        "entity_key"
      ]
    },
    "dim_geography": {
      "project": PROJECT,
      "filename": "dim_geography",
      "default": AutoloaderTable,
      "primary_keys": [
        "geography_key"
      ]
    },
    "dim_machine": {
      "project": PROJECT,
      "filename": "dim_machine",
      "default": AutoloaderTable,
      "primary_keys": [
        "machine_key"
      ]
    },
    "dim_outage": {
      "project": PROJECT,
      "filename": "dim_outage",
      "default": AutoloaderTable,
      "primary_keys": [
        "outage_key"
      ]
    },
    "dim_product": {
      "project": PROJECT,
      "filename": "dim_product",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_key"
      ]
    },
    "dim_product_category": {
      "project": PROJECT,
      "filename": "dim_product_category",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_category_key"
      ]
    },
    "dim_product_sub_category": {
      "project": PROJECT,
      "filename": "dim_product_sub_category",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_subcategory_key"
      ]
    },
    "dim_promotion": {
      "project": PROJECT,
      "filename": "dim_promotion",
      "default": AutoloaderTable,
      "primary_keys": [
        "promotion_key"
      ]
    },
    "dim_sales_territory": {
      "project": PROJECT,
      "filename": "dim_sales_territory",
      "default": AutoloaderTable,
      "primary_keys": [
        "sales_territory_key"
      ]
    },
    "dim_scenario": {
      "project": PROJECT,
      "filename": "dim_scenario",
      "default": AutoloaderTable,
      "primary_keys": [
        "scenario_key"
      ]
    },
    "dim_store": {
      "project": PROJECT,
      "filename": "dim_store",
      "default": AutoloaderTable,
      "primary_keys": [
        "store_key"
      ]
    },
    "fact_exchange_rate": {
      "project": PROJECT,
      "filename": "fact_exchange_rate",
      "default": AutoloaderTable,
      "primary_keys": [
        "exchange_rate_key"
      ]
    },
    "fact_inventory": {
      "project": PROJECT,
      "filename": "fact_inventory",
      "default": AutoloaderTable,
      "primary_keys": [
        "inventory_key"
      ]
    },
    "fact_it_machine": {
      "project": PROJECT,
      "filename": "fact_it_machine",
      "default": AutoloaderTable,
      "primary_keys": [
        "it_machine_key"
      ]
    },
    "fact_it_sla": {
      "project": PROJECT,
      "filename": "fact_it_sla",
      "default": AutoloaderTable,
      "primary_keys": [
        "it_sla_key"
      ]
    },
    "fact_online_sales": {
      "project": PROJECT,
      "filename": "fact_online_sales",
      "default": AutoloaderTable,
      "primary_keys": [
        "online_sales_key"
      ]
    },
    "fact_sales": {
      "project": PROJECT,
      "filename": "fact_sales",
      "default": AutoloaderTable,
      "primary_keys": [
        "sales_key"
      ]
    },
    "fact_sales_quota": {
      "project": PROJECT,
      "filename": "fact_sales_quota",
      "default": AutoloaderTable,
      "primary_keys": [
        "sales_quota_key"
      ]
    },
    "fact_strategy_plan": {
      "project": PROJECT,
      "filename": "fact_strategy_plan",
      "default": AutoloaderTable,
      "primary_keys": [
        "strategy_planning_key"
      ]
    }
  }