  
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
        "AccountKey"
      ]
    },
    "dim_channel": {
      "project": PROJECT,
      "filename": "dim_channel",
      "default": AutoloaderTable,
      "primary_keys": [
        "ChannelKey"
      ]
    },
    "dim_currency": {
      "project": PROJECT,
      "filename": "dim_currency",
      "default": AutoloaderTable,
      "primary_keys": [
        "CurrencyKey"
      ]
    },
    "dim_customer": {
      "project": PROJECT,
      "filename": "dim_customer",
      "default": AutoloaderTable,
      "primary_keys": [
        "CustomerKey"
      ]
    },
    "dim_date": {
      "project": PROJECT,
      "filename": "dim_date",
      "default": AutoloaderTable,
      "primary_keys": [
        "Datekey"
      ]
    },
    "dim_employee": {
      "project": PROJECT,
      "filename": "dim_employee",
      "default": AutoloaderTable,
      "primary_keys": [
        "EmployeeKey"
      ]
    },
    "dim_entity": {
      "project": PROJECT,
      "filename": "dim_entity",
      "default": AutoloaderTable,
      "primary_keys": [
        "EntityKey"
      ]
    },
    "dim_geography": {
      "project": PROJECT,
      "filename": "dim_geography",
      "default": AutoloaderTable,
      "primary_keys": [
        "GeographyKey"
      ]
    },
    "dim_machine": {
      "project": PROJECT,
      "filename": "dim_machine",
      "default": AutoloaderTable,
      "primary_keys": [
        "MachineKey"
      ]
    },
    "dim_outage": {
      "project": PROJECT,
      "filename": "dim_outage",
      "default": AutoloaderTable,
      "primary_keys": [
        "OutageKey"
      ]
    },
    "dim_product": {
      "project": PROJECT,
      "filename": "dim_product",
      "default": AutoloaderTable,
      "primary_keys": [
        "ProductKey"
      ]
    },
    "dim_product_category": {
      "project": PROJECT,
      "filename": "dim_product_category",
      "default": AutoloaderTable,
      "primary_keys": [
        "ProductCategoryKey"
      ]
    },
    "dim_product_sub_category": {
      "project": PROJECT,
      "filename": "dim_product_sub_category",
      "default": AutoloaderTable,
      "primary_keys": [
        "ProductSubcategoryKey"
      ]
    },
    "dim_promotion": {
      "project": PROJECT,
      "filename": "dim_promotion",
      "default": AutoloaderTable,
      "primary_keys": [
        "PromotionKey"
      ]
    },
    "dim_sales_territory": {
      "project": PROJECT,
      "filename": "dim_sales_territory",
      "default": AutoloaderTable,
      "primary_keys": [
        "SalesTerritoryKey"
      ]
    },
    "dim_scenario": {
      "project": PROJECT,
      "filename": "dim_scenario",
      "default": AutoloaderTable,
      "primary_keys": [
        "ScenarioKey"
      ]
    },
    "dim_store": {
      "project": PROJECT,
      "filename": "dim_store",
      "default": AutoloaderTable,
      "primary_keys": [
        "StoreKey"
      ]
    },
    "fact_exchange_rate": {
      "project": PROJECT,
      "filename": "fact_exchange_rate",
      "default": AutoloaderTable,
      "primary_keys": [
        "ExchangeRateKey"
      ]
    },
    "fact_inventory": {
      "project": PROJECT,
      "filename": "fact_inventory",
      "default": AutoloaderTable,
      "primary_keys": [
        "InventoryKey"
      ]
    },
    "fact_it_machine": {
      "project": PROJECT,
      "filename": "fact_it_machine",
      "default": AutoloaderTable,
      "primary_keys": [
        "ITMachinekey"
      ]
    },
    "fact_it_sla": {
      "project": PROJECT,
      "filename": "fact_it_sla",
      "default": AutoloaderTable,
      "primary_keys": [
        "ITSLAkey"
      ]
    },
    "fact_online_sales": {
      "project": PROJECT,
      "filename": "fact_online_sales",
      "default": AutoloaderTable,
      "primary_keys": [
        "OnlineSalesKey"
      ]
    },
    "fact_sales": {
      "project": PROJECT,
      "filename": "fact_sales",
      "default": AutoloaderTable,
      "primary_keys": [
        "SalesKey"
      ]
    },
    "fact_sales_quota": {
      "project": PROJECT,
      "filename": "fact_sales_quota",
      "default": AutoloaderTable,
      "primary_keys": [
        "SalesQuotaKey"
      ]
    },
    "fact_strategy_plan": {
      "project": PROJECT,
      "filename": "fact_strategy_plan",
      "default": AutoloaderTable,
      "primary_keys": [
        "StrategyPlanKey"
      ]
    }
  }