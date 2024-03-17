create table if not exists {{ database }}.{{ table }} 
(
    _corrupt_record string,
    _snapshot_date date not null,
    _process_id bigint not null,
    _load_date timestamp,
    _metadata struct<
      file_path: string,
      file_name: string,
      file_size: bigint,
      file_modification_time: timestamp,
      file_block_start: bigint,
      file_block_length: bigint
    >
)
USING DELTA
TBLPROPERTIES (
  delta.appendOnly = true
)