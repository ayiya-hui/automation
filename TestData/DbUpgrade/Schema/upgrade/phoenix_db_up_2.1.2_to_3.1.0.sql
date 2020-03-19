\set ON_ERROR_STOP on

--
-- new table
--
-- Table: ph_logical_conn

-- DROP TABLE ph_logical_conn;

CREATE TABLE ph_logical_conn
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  dest_host character varying(255),
  dir boolean,
  param text,
  port character varying(255),
  port_name character varying(255),
  proto character varying(255),
  src_host character varying(255),
  CONSTRAINT ph_logical_conn_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_logical_conn OWNER TO phoenix;

-- Table: ph_conn_port

-- DROP TABLE ph_conn_port;

CREATE TABLE ph_conn_port
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  loggedin character varying(255),
  registered character varying(255),
  san_controller_port_id bigint,
  storage_host_id bigint,
  CONSTRAINT ph_conn_port_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_conn_port OWNER TO phoenix;

CREATE TABLE ph_controller_port
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  port integer NOT NULL,
  processor character varying(255),
  device_id bigint,
  CONSTRAINT ph_controller_port_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_controller_port OWNER TO phoenix;

-- Table: ph_dev_maintenance

-- DROP TABLE ph_dev_maintenance;

CREATE TABLE ph_dev_maintenance
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  active boolean NOT NULL DEFAULT true,
  description character varying(2048),
  fireincidents boolean NOT NULL,
  "name" character varying(255),
  schedule text,
  CONSTRAINT ph_dev_maintenance_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_dev_maintenance OWNER TO phoenix;

-- Table: ph_dev_maintenance_item

-- DROP TABLE ph_dev_maintenance_item;

CREATE TABLE ph_dev_maintenance_item
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  item_id bigint,
  "type" integer,
  dev_maintenance_id bigint,
  CONSTRAINT ph_dev_maintenance_item_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_dev_maintenance_item OWNER TO phoenix;

-- Table: ph_dev_maintenance_status_mapping

-- DROP TABLE ph_dev_maintenance_status_mapping;

CREATE TABLE ph_dev_maintenance_status_mapping
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  device_id bigint,
  dev_maintenance_id bigint,
  status integer,
  CONSTRAINT ph_dev_maintenance_status_mapping_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_dev_maintenance_status_mapping OWNER TO phoenix;

-- Table: ph_devmain_grp_mapping

-- DROP TABLE ph_devmain_grp_mapping;

CREATE TABLE ph_devmain_grp_mapping
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  dev_maintenance_id bigint,
  group_id bigint,
  CONSTRAINT ph_devmain_grp_mapping_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_devmain_grp_mapping OWNER TO phoenix;

-- Table: ph_email_template

-- DROP TABLE ph_email_template;

CREATE TABLE ph_email_template
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  "name" character varying(255),
  pattern text,
  subject character varying(255),
  "type" integer,
  used boolean,
  CONSTRAINT ph_email_template_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_email_template OWNER TO phoenix;

-- Table: ph_group_properties

-- DROP TABLE ph_group_properties;

CREATE TABLE ph_group_properties
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  group_id bigint,
  property_name text,
  property_value character varying(1024),
  CONSTRAINT ph_group_properties_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_group_properties OWNER TO phoenix;

CREATE TABLE ph_lun
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  capacity integer,
  "name" character varying(255),
  "number" integer NOT NULL,
  lun_state character varying(255),
  device_id bigint,
  raid_group_id bigint,
  CONSTRAINT ph_lun_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_lun OWNER TO phoenix;

-- Table: ph_raid_group

-- DROP TABLE ph_raid_group;

CREATE TABLE ph_raid_group
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  logical_capacity_blocks bigint,
  logical_capacity_mb bigint,
  raid_group_id integer,
  raid_type character varying(255),
  raw_capacity_blocks bigint,
  raw_capacity_mb bigint,
  raid_group_state character varying(255),
  device_id bigint,
  CONSTRAINT ph_raid_group_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_raid_group OWNER TO phoenix;

-- Table: ph_raid_group2ph_device_comp

-- DROP TABLE ph_raid_group2ph_device_comp;

CREATE TABLE ph_raid_group2ph_device_comp
(
  raid_group_id bigint NOT NULL,
  component_id bigint NOT NULL
)
WITHOUT OIDS;
ALTER TABLE ph_raid_group2ph_device_comp OWNER TO phoenix;

-- Table: ph_rbac_profile

-- DROP TABLE ph_rbac_profile;

CREATE TABLE ph_rbac_profile
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  config text,
  description character varying(2048),
  "name" character varying(255),
  event_filter_id bigint,
  CONSTRAINT ph_rbac_profile_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_rbac_profile OWNER TO phoenix;

-- Table: ph_storage_group

-- DROP TABLE ph_storage_group;

CREATE TABLE ph_storage_group
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  "name" character varying(255),
  wwn character varying(255),
  device_id bigint,
  CONSTRAINT ph_storage_group_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_storage_group OWNER TO phoenix;

-- Table: ph_storage_group2ph_lun

-- DROP TABLE ph_storage_group2ph_lun;

CREATE TABLE ph_storage_group2ph_lun
(
  storage_group_id bigint NOT NULL,
  lun_id bigint NOT NULL
)
WITHOUT OIDS;
ALTER TABLE ph_storage_group2ph_lun OWNER TO phoenix;

-- Table: ph_storage_group2ph_storage_host

-- DROP TABLE ph_storage_group2ph_storage_host;

CREATE TABLE ph_storage_group2ph_storage_host
(
  storage_group_id bigint NOT NULL,
  storage_host_id bigint NOT NULL
)
WITHOUT OIDS;
ALTER TABLE ph_storage_group2ph_storage_host OWNER TO phoenix;

-- Table: ph_storage_host

-- DROP TABLE ph_storage_host;

CREATE TABLE ph_storage_host
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  ipv4_addr character varying(255),
  hostname character varying(255),
  model character varying(255),
  vendor character varying(255),
  wwn character varying(255),
  CONSTRAINT ph_storage_host_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_storage_host OWNER TO phoenix;

-- Table: ph_user_domain_mapping

-- DROP TABLE ph_user_domain_mapping;

CREATE TABLE ph_user_domain_mapping
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  domain_id bigint,
  user_id bigint,
  CONSTRAINT ph_user_domain_mapping_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_user_domain_mapping OWNER TO phoenix;

-- Table: ph_user_domain_profile_mapping

-- DROP TABLE ph_user_domain_profile_mapping;

CREATE TABLE ph_user_domain_profile_mapping
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  domain_id bigint,
  profile_id bigint,
  user_id bigint,
  CONSTRAINT ph_user_domain_profile_mapping_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_user_domain_profile_mapping OWNER TO phoenix;

--
-- new colums
--
alter table ph_app add column app_grp_name character varying(1024);
alter table ph_app_pkg add column path text;
alter table ph_app_pkg add column update_method character varying(255);
alter table ph_device add column department character varying(255);
alter table ph_device add column maintenance integer;
alter table ph_device_comp add column disksize character varying(255);
alter table ph_device_comp add column "type" character varying(255);
alter table ph_device_intf add column update_method character varying(255);
alter table ph_disc_ip_range add column no_ping boolean;
alter table ph_disc_profile add column no_ping text;
alter table ph_disc_profile add column no_root_ping text;
alter table ph_event_attr_type add column used_by_rbac boolean;
alter table ph_monitor_config add column frequency integer;
alter table ph_user add column prime_profile_id bigint;
alter table ph_schedule add column user_id bigint;

--
-- constraints
--

ALTER TABLE ph_conn_port ADD CONSTRAINT fk5f0d302da7c06a06 FOREIGN KEY (storage_host_id)
      REFERENCES ph_storage_host (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_conn_port ADD CONSTRAINT fk5f0d302db4045b27 FOREIGN KEY (san_controller_port_id)
      REFERENCES ph_controller_port (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_controller_port ADD CONSTRAINT fk622142fd94ed2ae5 FOREIGN KEY (device_id)
      REFERENCES ph_device (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_dev_maintenance_item ADD CONSTRAINT fk53cb1790170d9843 FOREIGN KEY (dev_maintenance_id)
      REFERENCES ph_dev_maintenance (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_lun ADD CONSTRAINT fkc505253e64238c3a FOREIGN KEY (raid_group_id)
      REFERENCES ph_raid_group (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_lun ADD CONSTRAINT fkc505253e94ed2ae5 FOREIGN KEY (device_id)
      REFERENCES ph_device (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_raid_group2ph_device_comp ADD CONSTRAINT fk2df1e1f264238c3a FOREIGN KEY (raid_group_id)
      REFERENCES ph_raid_group (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_raid_group2ph_device_comp ADD CONSTRAINT fk2df1e1f26c3c67cf FOREIGN KEY (component_id)
      REFERENCES ph_device_comp (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_rbac_profile ADD CONSTRAINT fk61c8dba3d092eafc FOREIGN KEY (event_filter_id)
      REFERENCES ph_drq_filter (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_storage_group ADD CONSTRAINT fk7bd4a1b494ed2ae5 FOREIGN KEY (device_id)
      REFERENCES ph_device (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_storage_group2ph_lun ADD CONSTRAINT fk24c50bfc4b6e768f FOREIGN KEY (lun_id)
      REFERENCES ph_lun (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_storage_group2ph_lun ADD CONSTRAINT fk24c50bfc8053dd8e FOREIGN KEY (storage_group_id)
      REFERENCES ph_storage_group (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_storage_group2ph_storage_host ADD CONSTRAINT fk540b2f58053dd8e FOREIGN KEY (storage_group_id)
      REFERENCES ph_storage_group (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_storage_group2ph_storage_host ADD CONSTRAINT fk540b2f5a7c06a06 FOREIGN KEY (storage_host_id)
      REFERENCES ph_storage_host (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_user ADD CONSTRAINT fkdba391b222971359 FOREIGN KEY (prime_profile_id)
      REFERENCES ph_rbac_profile (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_user_domain_mapping ADD CONSTRAINT fkd541928011014d73 FOREIGN KEY (user_id)
      REFERENCES ph_user (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_user_domain_mapping ADD CONSTRAINT fkd541928024fdbf36 FOREIGN KEY (domain_id)
      REFERENCES ph_sys_domain (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_user_domain_profile_mapping ADD CONSTRAINT fkad0037ea11014d73 FOREIGN KEY (user_id)
      REFERENCES ph_user (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_user_domain_profile_mapping ADD CONSTRAINT fkad0037ea24fdbf36 FOREIGN KEY (domain_id)
      REFERENCES ph_sys_domain (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_user_domain_profile_mapping ADD CONSTRAINT fkad0037eaf35aa599 FOREIGN KEY (profile_id)
      REFERENCES ph_rbac_profile (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_mon_perf_obj ALTER COLUMN threshold type real;

ALTER TABLE ph_mon_template_item ALTER COLUMN threshold type real;


--
-- drop constraints
--

ALTER TABLE ph_device drop CONSTRAINT "ph_device2ph_sys_collector_agentId";

--
-- data migration
--
--delete old event types

delete from ph_group_item where item_id in (select id from ph_event_type where name ~ 'Juniper_IDP-[0-9]');
delete from ph_event_type where name ~ 'Juniper_IDP-[0-9]';

--
-- update db version
--
update ph_sys_conf set value = '3.1.0' where property = 'DB_Schema_Version';
