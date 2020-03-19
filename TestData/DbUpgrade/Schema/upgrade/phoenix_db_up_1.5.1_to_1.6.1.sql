\set ON_ERROR_STOP on

--
-- Tables
--

-- Table: ph_mon_oid

CREATE TABLE ph_mon_oid
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  attribute character varying(255),
  "value" character varying(255),
  CONSTRAINT ph_mon_oid_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_mon_oid OWNER TO phoenix;


-- Table: ph_mon_perf_obj2oid

CREATE TABLE ph_mon_perf_obj2oid
(
  perf_obj_id bigint NOT NULL,
  oid_id bigint NOT NULL,
  CONSTRAINT fk777a7c33241fc2f1 FOREIGN KEY (oid_id)
      REFERENCES ph_mon_oid (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk777a7c3371a92fba FOREIGN KEY (perf_obj_id)
      REFERENCES ph_mon_perf_obj (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITHOUT OIDS;
ALTER TABLE ph_mon_perf_obj2oid OWNER TO phoenix;

-- Table: ph_svc_mon

CREATE TABLE ph_svc_mon
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  appname character varying(255),
  description character varying(255),
  host_addr character varying(255),
  "name" character varying(255),
  svc_ports character varying(255),
  time_interval integer,
  CONSTRAINT ph_svc_mon_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_svc_mon OWNER TO phoenix;

-- Table: ph_svc_probe_ss

CREATE TABLE ph_svc_probe_ss
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  description character varying(255),
  "name" character varying(255),
  time_interval integer,
  CONSTRAINT ph_svc_probe_ss_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_svc_probe_ss OWNER TO phoenix;

-- Table: ph_svc_mon2svc_probe_ss

CREATE TABLE ph_svc_mon2svc_probe_ss
(
  svc_mon_id bigint NOT NULL,
  svc_probe_ss_id bigint NOT NULL,
  CONSTRAINT fk92a885da717d699c FOREIGN KEY (svc_probe_ss_id)
      REFERENCES ph_svc_probe_ss (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk92a885da94661add FOREIGN KEY (svc_mon_id)
      REFERENCES ph_svc_mon (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITHOUT OIDS;
ALTER TABLE ph_svc_mon2svc_probe_ss OWNER TO phoenix;

-- Table: ph_svc_probe

CREATE TABLE ph_svc_probe
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  config text,
  "index" integer NOT NULL,
  session_id bigint,
  CONSTRAINT ph_svc_probe_pkey PRIMARY KEY (id),
  CONSTRAINT fk1bef938ac109ce54 FOREIGN KEY (session_id)
      REFERENCES ph_svc_probe_ss (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITHOUT OIDS;
ALTER TABLE ph_svc_probe OWNER TO phoenix;

-- Table: ph_layer2_conn

CREATE TABLE ph_layer2_conn
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  intf1 character varying(255),
  intf2 character varying(255),
  name1 character varying(255),
  name2 character varying(255),
  vlan character varying(255),
  CONSTRAINT ph_layer2_conn_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_layer2_conn OWNER TO phoenix;

--
-- Add columns
--

ALTER TABLE ph_app_pkg ADD COLUMN app_grp_name character varying(255);
ALTER TABLE ph_app_pkg ADD COLUMN priority integer;

ALTER TABLE ph_device ADD COLUMN approved boolean;
ALTER TABLE ph_device ADD COLUMN hw_serial_no character varying(255);
ALTER TABLE ph_device ADD COLUMN hw_vendor character varying(255);
ALTER TABLE ph_device ADD COLUMN annotation character varying(512);

ALTER TABLE ph_mon_perf_obj ADD COLUMN natural_id character varying(255);

ALTER TABLE ph_monitor_config ADD COLUMN data_id bigint;
ALTER TABLE ph_monitor_config ADD COLUMN data_type integer;
ALTER TABLE ph_monitor_config ADD COLUMN param character varying(512);

ALTER TABLE ph_task ADD COLUMN gateway character varying(255);

ALTER TABLE ph_change_set ADD COLUMN natural_id character varying(255);

ALTER TABLE ph_topo_node ALTER COLUMN param type text;

ALTER TABLE ph_event_type ALTER COLUMN cve_codes type character varying(1024);

--
-- update columns
--

update ph_device_access set access_proto=replace(access_proto, 'SOAP','VM_SDK');
update ph_device set creation_method=replace(creation_method, 'SOAP','VM SDK'), discover_method=replace(discover_method, 'SOAP','VM SDK'), update_method=replace(update_method, 'SOAP','VM SDK');
update ph_device set approved=TRUE;
update ph_device_type set access_protos=replace(access_protos, 'SOAP','VM_SDK');

--
-- drop constraints
--

ALTER TABLE ph_monitor_config DROP CONSTRAINT ph_monitor_config2mon_ferf_fk;
ALTER TABLE ph_sys_conf DROP CONSTRAINT ph_sys_conf_unique_key;
ALTER TABLE ph_sys_conf ADD CONSTRAINT ph_sys_conf_unique_key UNIQUE (cust_org_id, category, property, owner_id);

--
-- drop columns
--

ALTER TABLE ph_monitor_config DROP COLUMN perf_object_id;

--
-- clean up perf monitor templates
--

delete from ph_mon_template_item;
delete from ph_mon_template2device_type;
delete from ph_mon_template;
delete from ph_mon_perf_obj;
delete from ph_monitor_config;

--
-- add index
--
CREATE INDEX ph_group_item_item_id_index
  ON ph_group_item
  USING btree
  (item_id);

--
-- update db version
--
update ph_sys_conf set value = '1.6.1' where property = 'DB_Schema_Version';
