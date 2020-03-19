\set ON_ERROR_STOP on


Update ph_drq_rule set active = 'f' where cust_org_id = 0 and name like '%(Internal)%';

delete from ph_group_item where item_id in (select id from ph_event_type where name like 'PH_RULE_%') and group_id not in (select id from ph_group where name like 'PH_SYS_EVENT_PH_RULE_%');

ALTER TABLE ph_incident ALTER COLUMN orig_device_ip type text;

ALTER TABLE ph_incident ALTER COLUMN view_users type text;

--
-- update db version
--
update ph_sys_conf set value = '2.1.1' where property = 'DB_Schema_Version';
