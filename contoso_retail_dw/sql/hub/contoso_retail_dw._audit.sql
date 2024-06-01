create table if not exists {{database}}._audit 
(
    `table` string not null,
    total_count bigint not null,
    valid_count bigint not null,
    invalid_count bigint not null,
    invalid_ratio double not null,
    file_path string not null,
    file_name string not null,
    file_size bigint not null,
    file_modification_time timestamp not null,
    schema_valid boolean not null,
    snapshot_date date not null,
    process_id bigint not null,
    stage_load_date timestamp not null,
    hub_load_date timestamp
)
USING DELTA
TBLPROPERTIES (
  delta.appendOnly = true
)