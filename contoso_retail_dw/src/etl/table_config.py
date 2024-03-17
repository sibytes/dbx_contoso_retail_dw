  
from ._table_autoloader import AutoloaderTable

PROJECT = "contoso_retail_dw"
# register tables here and map them to a table Class
# if adding new properties then they must be added
# to the __init__ of the ._base_table.BaseTable
def tables():

  return {
    "hr_department": {
      "project": PROJECT,
      "filename": "humanresources_department",
      "default": AutoloaderTable,
      "primary_keys": [
        "department_id"
      ]
    },
    "hr_employee": {
      "project": PROJECT,
      "filename": "humanresources_employee",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_ID"
      ]
    },
    "hr_employee_department_history": {
      "project": PROJECT,
      "filename": "humanresources_employeedepartmenthistory",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id",
        "department_id",
        "shift_id",
        "start_date"
      ]
    },
    "hr_employee_pay_history": {
      "project": PROJECT,
      "filename": "humanresources_employeepayhistory",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id",
        "rate_change_date"
      ]
    },
    # "hr_job_candidate": {
    #   "project": PROJECT,
    #   "filename": "humanresources_jobcandidate",
    #   "default": AutoloaderTable,
    #   "primary_keys": [
    #     "job_candidate_date"
    #   ]
    # },
    "hr_shift": {
      "project": PROJECT,
      "filename": "humanresources_shift",
      "default": AutoloaderTable,
      "primary_keys": [
        "shift_id"
      ]
    },
    "person_address": {
      "project": PROJECT,
      "filename": "person__vaddress",
      "default": AutoloaderTable,
      "primary_keys": [
        "address_id"
      ]
    },
    "person_address_type": {
      "project": PROJECT,
      "filename": "person_addresstype",
      "default": AutoloaderTable,
      "primary_keys": [
        "address_type_id"
      ]
    },
    "person_business_entity": {
      "project": PROJECT,
      "filename": "person_businessentity",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id"
      ]
    },
    "person_business_entity_address": {
      "project": PROJECT,
      "filename": "person_businessentityaddress",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id",
        "address_id",
        "address_type_id"
      ]
    },
    "person_business_entity_contact": {
      "project": PROJECT,
      "filename": "person_businessentitycontact",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id",
        "person_id",
        "contact_type_id"
      ]
    },
    "person_contact_type": {
      "project": PROJECT,
      "filename": "person_contacttype",
      "default": AutoloaderTable,
      "primary_keys": [
        "contact_type_id"
      ]
    },
    "person_country_region": {
      "project": PROJECT,
      "filename": "person_countryregion",
      "default": AutoloaderTable,
      "primary_keys": [
        "country_region_code"
      ]
    },
    "person_email_address": {
      "project": PROJECT,
      "filename": "person_emailaddress",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id",
        "email_address_id"
      ]
    },
    "person_password": {
      "project": PROJECT,
      "filename": "person_password",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id"
      ]
    },
    "person_person": {
      "project": PROJECT,
      "filename": "person_person",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id"
      ]
    },
    "person_person_phone": {
      "project": PROJECT,
      "filename": "person_personphone",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id",
        "phone_number",
        "phone_number_type_id"
      ]
    },
    "person_phone_number_type": {
      "project": PROJECT,
      "filename": "person_phonenumbertype",
      "default": AutoloaderTable,
      "primary_keys": [
        "phone_number_type_id"
      ]
    },
    "person_state_province": {
      "project": PROJECT,
      "filename": "person_stateprovince",
      "default": AutoloaderTable,
      "primary_keys": [
        "state_province_id"
      ]
    },
    "production_bill_of_materials": {
      "project": PROJECT,
      "filename": "production_billofmaterials",
      "default": AutoloaderTable,
      "primary_keys": [
        "bill_of_materials_id"
      ]
    },
    "production_culture": {
      "project": PROJECT,
      "filename": "production_culture",
      "default": AutoloaderTable,
      "primary_keys": [
        "culture_id"
      ]
    },
    # "production_document": {
    #   "project": PROJECT,
    #   "filename": "production__vdocument",
    #   "default": AutoloaderTable,
    #   "primary_keys": [
    #     "document_node"
    #   ]
    # },
    "production_illustration": {
      "project": PROJECT,
      "filename": "production_illustration",
      "default": AutoloaderTable,
      "primary_keys": [
        "illustration_id"
      ]
    },
    "production_location": {
      "project": PROJECT,
      "filename": "production_location",
      "default": AutoloaderTable,
      "primary_keys": [
        "location_id"
      ]
    },
    "production_product": {
      "project": PROJECT,
      "filename": "production_product",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_id"
      ]
    },
    "production_product_category": {
      "project": PROJECT,
      "filename": "production_productcategory",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_category_id"
      ]
    },
    "production_product_cost_history": {
      "project": PROJECT,
      "filename": "production_productcosthistory",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_id",
        "start_date"
      ]
    },
    "production_product_description": {
      "project": PROJECT,
      "filename": "production_productdescription",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_description_id"
      ]
    },
    "production_product_document": {
      "project": PROJECT,
      "filename": "production__vproductdocument",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_id",
        "document_node"
      ]
    },
    "production_product_inventory": {
      "project": PROJECT,
      "filename": "production_productinventory",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_id",
        "location_id"
      ]
    },
    "production_product_list_price_history": {
      "project": PROJECT,
      "filename": "production_productlistpricehistory",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_id",
        "start_date"
      ]
    },
    # "production_product_model": {
    #   "project": PROJECT,
    #   "filename": "production_productmodel",
    #   "default": AutoloaderTable,
    #   "primary_keys": [
    #     "product_model_id"
    #   ]
    # },
    "production_product_model_illustration": {
      "project": PROJECT,
      "filename": "production_productmodelillustration",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_model_id",
        "illustration_id"
      ]
    },
    "production_product_model_product_description_culture": {
      "project": PROJECT,
      "filename": "production_productmodelproductdescriptionculture",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_model_id",
        "product_description_id",
        "culture_id"
      ]
    },
    "production_product_photo": {
      "project": PROJECT,
      "filename": "production_productphoto",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_photo_id"
      ]
    },
    "production_product_product_photo": {
      "project": PROJECT,
      "filename": "production_productproductphoto",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_id",
        "product_photo_id"
      ]
    },
    # "production_product_review": {
    #   "project": PROJECT,
    #   "filename": "production_productreview",
    #   "default": AutoloaderTable,
    #   "primary_keys": [
    #     "product_review_id"
    #   ]
    # },
    "production_product_subcategory": {
      "project": PROJECT,
      "filename": "production_productsubcategory",
      "default": AutoloaderTable,
      "primary_keys": [
        "product_subcategory_id"
      ]
    },
    "production_scrap_reason": {
      "project": PROJECT,
      "filename": "production_scrapreason",
      "default": AutoloaderTable,
      "primary_keys": [
        "scrap_reason_id"
      ]
    },
    "production_transaction_history": {
      "project": PROJECT,
      "filename": "production_transactionhistory",
      "default": AutoloaderTable,
      "primary_keys": [
        "transaction_id"
      ]
    },
    "production_transaction_history_archive": {
      "project": PROJECT,
      "filename": "production_transactionhistoryarchive",
      "default": AutoloaderTable,
      "primary_keys": [
        "transaction_id"
      ]
    },
    "production_unit_measure": {
      "project": PROJECT,
      "filename": "production_unitmeasure",
      "default": AutoloaderTable,
      "primary_keys": [
        "unit_measure_code"
      ]
    },
    "production_work_order": {
      "project": PROJECT,
      "filename": "production_workorder",
      "default": AutoloaderTable,
      "primary_keys": [
        "work_order_id"
      ]
    },
    "production_work_order_routing": {
      "project": PROJECT,
      "filename": "production_workorderrouting",
      "default": AutoloaderTable,
      "primary_keys": [
        "work_order_id",
        "product_id",
        "operation_sequence"
      ]
    },
    "purchasing_product_vendor": {
      "project": PROJECT,
      "filename": "purchasing_productvendor",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id"
      ]
    },
    "purchasing_purchase_order_detail": {
      "project": PROJECT,
      "filename": "purchasing_purchaseorderdetail",
      "default": AutoloaderTable,
      "primary_keys": [
        "purchase_order_id",
        "purchase_order_detail_id"
      ]
    },
    "purchasing_purchase_order_header": {
      "project": PROJECT,
      "filename": "purchasing_purchaseorderheader",
      "default": AutoloaderTable,
      "primary_keys": [
        "purchase_order_id"
      ]
    },
    "purchasing_ship_method": {
      "project": PROJECT,
      "filename": "purchasing_shipmethod",
      "default": AutoloaderTable,
      "primary_keys": [
        "ship_method_id"
      ]
    },
    "purchasing_vendor": {
      "project": PROJECT,
      "filename": "purchasing_vendor",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id"
      ]
    },
    "sales_country_region_currency": {
      "project": PROJECT,
      "filename": "sales_countryregioncurrency",
      "default": AutoloaderTable,
      "primary_keys": [
        "country_region_code",
        "currency_code"
      ]
    },
    "sales_credit_card": {
      "project": PROJECT,
      "filename": "sales_creditcard",
      "default": AutoloaderTable,
      "primary_keys": [
        "credit_card_id"
      ]
    },
    "sales_currency": {
      "project": PROJECT,
      "filename": "sales_currency",
      "default": AutoloaderTable,
      "primary_keys": [
        "currency_code"
      ]
    },
    "sales_currency_rate": {
      "project": PROJECT,
      "filename": "sales_currencyrate",
      "default": AutoloaderTable,
      "primary_keys": [
        "currency_rate_id"
      ]
    },
    "sales_customer": {
      "project": PROJECT,
      "filename": "sales_customer",
      "default": AutoloaderTable,
      "primary_keys": [
        "customer_id"
      ]
    },
    "sales_person_credit_card": {
      "project": PROJECT,
      "filename": "sales_personcreditcard",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id",
        "credit_card_id"
      ]
    },
    "sales_sales_order_detail": {
      "project": PROJECT,
      "filename": "sales_salesorderdetail",
      "default": AutoloaderTable,
      "primary_keys": [
        "sales_order_id",
        "sales_order_detail_id"
      ]
    },
    "sales_sales_order_header": {
      "project": PROJECT,
      "filename": "sales_salesorderheader",
      "default": AutoloaderTable,
      "primary_keys": [
        "sales_order_id"
      ]
    },
    "sales_sales_order_header_sales_reason": {
      "project": PROJECT,
      "filename": "sales_salesorderheadersalesreason",
      "default": AutoloaderTable,
      "primary_keys": [
        "sales_order_id",
        "sales_reason_id"
      ]
    },
    "sales_sales_person": {
      "project": PROJECT,
      "filename": "sales_salesperson",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id"
      ]
    },
    "sales_sales_person_quota_history": {
      "project": PROJECT,
      "filename": "sales_salespersonquotahistory",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id",
        "quota_date"
      ]
    },
    "sales_sales_reason": {
      "project": PROJECT,
      "filename": "sales_salesreason",
      "default": AutoloaderTable,
      "primary_keys": [
        "sales_reason_id"
      ]
    },
    "sales_sales_tax_rate": {
      "project": PROJECT,
      "filename": "sales_salestaxrate",
      "default": AutoloaderTable,
      "primary_keys": [
        "sales_tax_rate_id"
      ]
    },
    "sales_sales_territory": {
      "project": PROJECT,
      "filename": "sales_salesterritory",
      "default": AutoloaderTable,
      "primary_keys": [
        "territory_id"
      ]
    },
    "sales_sales_territory_history": {
      "project": PROJECT,
      "filename": "sales_salesterritoryhistory",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id",
        "territory_id",
        "start_date"
      ]
    },
    "sales_shopping_cart_item": {
      "project": PROJECT,
      "filename": "sales_shoppingcartitem",
      "default": AutoloaderTable,
      "primary_keys": [
        "shopping_cart_item_id"
      ]
    },
    "sales_special_offer": {
      "project": PROJECT,
      "filename": "sales_specialoffer",
      "default": AutoloaderTable,
      "primary_keys": [
        "special_offer_id"
      ]
    },
    "sales_special_offer_product": {
      "project": PROJECT,
      "filename": "sales_specialofferproduct",
      "default": AutoloaderTable,
      "primary_keys": [
        "special_offer_id",
        "product_id"
      ]
    },
    "sales_store": {
      "project": PROJECT,
      "filename": "sales_store",
      "default": AutoloaderTable,
      "primary_keys": [
        "business_entity_id"
      ]
    },
  }
