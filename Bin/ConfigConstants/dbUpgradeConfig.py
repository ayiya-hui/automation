CREATE_KEY='CREATE TABLE'
ALTER_KEY='ALTER TABLE'
REFERENCE_KEY='REFERENCE'
PATTERN_ADD_COLUMN='alter table\s+(?P<tableName>\S+)\s+add column\s+(?P<columnName>\S+)\s+(?P<dataType>[\s\S\(\)]+);'
PATTERN_CONSTR_OWEER='ALTER TABLE\s+(?P<tableName>\S+)\s+OWNER TO\s+(?P<tableOwner>\S+)'
PATTERN_CONSTR_PRIMARY='CONSTRAINT\s+(?P<constrName>\S+)\s+PRIMARY\s+KEY\s+\((?P<constrValue>\S+)[\s]?\)'
PATTERN_CONSTR_FOREIGN='ALTER TABLE\s+(?P<tableName>\S+)\s+ADD CONSTRAINT\s+(?P<keyName>[\S\d]+)\s+FOREIGN KEY\s+\((?P<columnName>\S+)\)'
PATTERN_REFERENCE='REFERENCES\s+(?P<refTableName>\S+)\s+(?P<refColumnName>[\(\)\S]+)\s+MATCH SIMPLE'
PATH='../TestData/DbUpgrade/Schema/upgrade/'
VERSIONS={'3.6.1':'phoenix_db_up_3.5.2_to_3.6.1.sql',
          '3.5.2':'phoenix_db_up_3.5.1_to_3.5.2.sql',
          '3.5.1':'phoenix_db_up_3.1.2_to_3.5.1.sql',
          '3.1.2':'phoenix_db_up_3.1.0_to_3.1.2.sql'}
TABLES="Select table_name from information_schema.TABLES where table_name like 'ph_%'"
TABLE_ATTR="Select column_name, is_nullable, data_type, character_maximum_length, column_default from information_schema.COLUMNS where table_name = '%s'"
NOTIFICATION="Select id, cust_org_id, event_source_id, name from ph_notification where event_source_type = 'Rule'"
DELIVER="Select receipt, receipt_type, type from ph_delivery where notification_id = %s"
RULE_NATURAL_ID="Select natural_id from ph_drq_rule where id = %s"
DB_VERSION="Select value from ph_sys_conf where property = 'DB_Schema_Version'"
