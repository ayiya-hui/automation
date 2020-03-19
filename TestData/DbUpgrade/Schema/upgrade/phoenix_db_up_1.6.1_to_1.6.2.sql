\set ON_ERROR_STOP on

--
-- Tables
--

--
-- Add columns
--

ALTER TABLE ph_group ADD COLUMN top_group boolean NOT NULL DEFAULT false;

--
-- Alter columns
--
ALTER TABLE ph_access_ip_range ALTER COLUMN exclude_range type text;
ALTER TABLE ph_access_ip_range ALTER COLUMN include_range type text;

ALTER TABLE ph_app ALTER COLUMN inst_path type text;
ALTER TABLE ph_app ALTER COLUMN proc_name type text;
ALTER TABLE ph_app ALTER COLUMN proc_param type text;
ALTER TABLE ph_app ALTER COLUMN services type text;
ALTER TABLE ph_app ALTER COLUMN sw_services type text;

ALTER TABLE ph_app_pkg ALTER COLUMN proc_name type text;
ALTER TABLE ph_app_pkg ALTER COLUMN proc_param type text;
ALTER TABLE ph_app_pkg ALTER COLUMN services type text;

ALTER TABLE ph_dev_event_attr ALTER COLUMN attrnamelist type text;

ALTER TABLE ph_device_access ALTER COLUMN param type text;

ALTER TABLE ph_device_sw_svc ALTER COLUMN exec_path type text;

ALTER TABLE ph_drq_report ALTER COLUMN relevant_filter_attr type text;

ALTER TABLE ph_filter_ip_range ALTER COLUMN exclude_range type text;
ALTER TABLE ph_filter_ip_range ALTER COLUMN include_range type text;

ALTER TABLE ph_ip_access_mapping ALTER COLUMN ip_range type text;

ALTER TABLE ph_malware_site ALTER COLUMN description type character varying(2048);

ALTER TABLE ph_monitor_type ALTER COLUMN description type character varying(2048);

ALTER TABLE ph_task ALTER COLUMN param_str type text;
--
-- drop constraints
--


--
-- drop columns
--

--
-- clean up perf monitor templates
--


--
-- add index
--

--
-- update db version
--
update ph_sys_conf set value = '1.6.2' where property = 'DB_Schema_Version';
