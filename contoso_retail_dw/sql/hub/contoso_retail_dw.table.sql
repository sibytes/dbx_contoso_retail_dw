create table if not exists {{ database }}.{{ table }} 
(
    {{ columns }},
    _snapshot_date timestamp not null,
    _process_id bigint not null,
    _load_date timestamp not null,
    _file_name string not null,
    _is_migration boolean not null,
    _from_date date not null,
    _to_date date not null,
    _is_current boolean not null
)
USING DELTA
TBLPROPERTIES (
    delta.enableChangeDataFeed = true
)
