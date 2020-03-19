\set ON_ERROR_STOP on

--
-- Alter columns
--

ALTER TABLE ph_change_set ALTER COLUMN item_name type text;
ALTER TABLE ph_change_set ALTER COLUMN natural_id type text;
ALTER TABLE ph_layer2_conn ALTER COLUMN vlan type text;

--
--clean up rule data
--
DELETE from ph_group_item where item_id in (select id from ph_event_type where name like 'PH_RULE_%');

--
-- update db version
--
update ph_sys_conf set value = '1.6.4' where property = 'DB_Schema_Version';
