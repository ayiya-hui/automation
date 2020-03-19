\set ON_ERROR_STOP on

--
-- new table
--

-- Table: ph_collector_cpu

-- DROP TABLE ph_collector_cpu;

CREATE TABLE ph_collector_cpu
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  cpu_id integer,
  cpu_load integer,
  collector_status_id bigint NOT NULL,
  display_order integer,
  CONSTRAINT ph_collector_cpu_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_collector_cpu OWNER TO phoenix;

-- Table: ph_collector_disk

-- DROP TABLE ph_collector_disk;

CREATE TABLE ph_collector_disk
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  disk_name character varying(255),
  disk_total bigint,
  disk_used bigint,
  collector_status_id bigint NOT NULL,
  display_order integer,
  CONSTRAINT ph_collector_disk_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_collector_disk OWNER TO phoenix;

-- Table: ph_collector_disk_io

-- DROP TABLE ph_collector_disk_io;

CREATE TABLE ph_collector_disk_io
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  app_latency real,
  latency real NOT NULL,
  disk_name character varying(255),
  rkbps real NOT NULL,
  rps real NOT NULL,
  util real NOT NULL,
  wkbps real NOT NULL,
  wps real NOT NULL,
  collector_status_id bigint NOT NULL,
  display_order integer,
  CONSTRAINT ph_collector_disk_io_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_collector_disk_io OWNER TO phoenix;


-- Table: ph_collector_mem_swap

-- DROP TABLE ph_collector_mem_swap;

CREATE TABLE ph_collector_mem_swap
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  swap_space bigint,
  swap_used bigint,
  collector_status_id bigint NOT NULL,
  display_order integer,
  CONSTRAINT ph_collector_mem_swap_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_collector_mem_swap OWNER TO phoenix;

-- Table: ph_collector_status

-- DROP TABLE ph_collector_status;

CREATE TABLE ph_collector_status
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  build_date bigint,
  collector_name character varying(255),
  cpu_util real,
  cust_name character varying(255),
  download_status character varying(255),
  health_status character varying(255),
  install_status character varying(255),
  ip_addr character varying(255),
  last_file_recv_time bigint,
  last_perf_data_time bigint,
  last_status_update_time bigint,
  mem_util real,
  status character varying(255),
  up_time bigint,
  upgrade_version character varying(255),
  "version" character varying(255),
  CONSTRAINT ph_collector_status_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_collector_status OWNER TO phoenix;

-- Table: ph_event_parser

-- DROP TABLE ph_event_parser;

CREATE TABLE ph_event_parser
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  description character varying(255),
  enabled boolean,
  "name" character varying(255),
  parser_xml text,
  sys_defined boolean,
  test_event character varying(255),
  device_type_id bigint,
  prev_parser_id bigint,
  CONSTRAINT ph_event_parser_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_event_parser OWNER TO phoenix;

-- Table: ph_l3_network_dep

-- DROP TABLE ph_l3_network_dep;

CREATE TABLE ph_l3_network_dep
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  discovered boolean,
  last_hop_dev_ip character varying(255),
  last_hop_dev_name character varying(255),
  network character varying(255),
  CONSTRAINT ph_l3_network_dep_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_l3_network_dep OWNER TO phoenix;

-- Table: ph_notification_action

-- DROP TABLE ph_notification_action;

CREATE TABLE ph_notification_action
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  action_definition text,
  action_type character varying(255),
  notification_policy_id bigint NOT NULL,
  display_order integer,
  CONSTRAINT ph_notification_action_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_notification_action OWNER TO phoenix;

-- Table: ph_notification_condition

-- DROP TABLE ph_notification_condition;

CREATE TABLE ph_notification_condition
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  included boolean NOT NULL DEFAULT true,
  condition_name character varying(255),
  condition_type character varying(255),
  notification_policy_id bigint NOT NULL,
  display_order integer,
  CONSTRAINT ph_notification_condition_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_notification_condition OWNER TO phoenix;

-- Table: ph_notification_policy

-- DROP TABLE ph_notification_policy;

CREATE TABLE ph_notification_policy
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  affected_items text,
  description text,
  display_order integer,
  enabled boolean NOT NULL DEFAULT true,
  exclude_affected_items text,
  exclude_target_orgs text,
  "name" character varying(255),
  severity character varying(255),
  target_orgs text,
  time_expr character varying(255),
  CONSTRAINT ph_notification_policy_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_notification_policy OWNER TO phoenix;

-- Table: ph_perf_transform

-- DROP TABLE ph_perf_transform;

CREATE TABLE ph_perf_transform
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  base_attr character varying(255),
  formula character varying(255),
  freq_attr character varying(255),
  "name" character varying(255),
  "type" character varying(255),
  oid_id bigint,
  CONSTRAINT ph_perf_transform_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_perf_transform OWNER TO phoenix;

-- Table: ph_sys_error

-- DROP TABLE ph_sys_error;

CREATE TABLE ph_sys_error
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  description character varying(255),
  error_obj_id character varying(255),
  error_obj_type character varying(255),
  error_source character varying(255),
  error_type character varying(255),
  occurred_time bigint,
  severity character varying(255),
  status character varying(255),
  status_change_time bigint,
  status_changed_by bigint,
  subject character varying(255),
  CONSTRAINT ph_sys_error_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_sys_error OWNER TO phoenix;

-- Table: ph_dev_ip_hostname

-- DROP TABLE ph_dev_ip_hostname;

CREATE TABLE ph_dev_ip_hostname
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  host_name character varying(255),
  ipv4_addr character varying(255),
  ipv6_addr character varying(255),
  device_id bigint,
  CONSTRAINT ph_dev_ip_hostname_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_dev_ip_hostname OWNER TO phoenix;

-- Table: ph_cust_property_def

-- DROP TABLE ph_cust_property_def;

CREATE TABLE ph_cust_property_def
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  display_name character varying(255),
  object_type integer,
  property_name character varying(255),
  property_type integer,
  value_type integer,
  CONSTRAINT ph_cust_property_def_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_cust_property_def OWNER TO phoenix;

-- Table: ph_cust_property

-- DROP TABLE ph_cust_property;

CREATE TABLE ph_cust_property
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  obj_id bigint,
  property_value character varying(1024),
  property_def_id bigint,
  CONSTRAINT ph_cust_property_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_cust_property OWNER TO phoenix;

--
-- new colums
--

alter table ph_alert add column sound text;
alter table ph_device_ep_access add column status integer;
alter table ph_device_ep_access add column status_desc text;
alter table ph_device_type add column sys_defined boolean;
alter table ph_drq_rule add column ph_incident_category character varying(255);
alter table ph_event_attr_type add column sys_defined boolean;
alter table ph_event_type add column sys_defined boolean;
alter table ph_mon_oid add column alias character varying(255);
alter table ph_mon_oid add column eat_name character varying(255);
alter table ph_mon_oid add column format character varying(255);
alter table ph_mon_oid add column sys_defined boolean;
alter table ph_mon_oid add column transform_order character varying(255);
alter table ph_mon_oid add column "type" character varying(255);
alter table ph_mon_perf_obj add column et_name character varying(255);
alter table ph_mon_perf_obj add column parent_oid character varying(255);
alter table ph_mon_perf_obj add column parent_oid_is_table boolean;
alter table ph_mon_perf_obj add column sys_defined boolean;
alter table ph_mon_perf_obj add column "name" character varying(255);
alter table ph_mon_template add column sys_defined boolean;
alter table ph_monitor_config add column status integer;
alter table ph_monitor_config add column status_desc text;
alter table ph_disc_ip_range add column ping_only boolean;
alter table ph_device add column sec_context character varying(255);
alter table ph_drq_report add column output_constraint character varying(255);
alter table ph_drq_report add column output_lines integer;
alter table ph_incident add column external_assigned_user character varying(255);
alter table ph_incident add column external_clear_time bigint;
alter table ph_incident add column external_ticket_id character varying(255);
alter table ph_incident add column external_ticket_state character varying(255);
alter table ph_incident add column external_ticket_type character varying(255);
alter table ph_incident add column notification_action_status text;
alter table ph_incident add column ph_incident_category character varying(255);

--
-- constraints
--

ALTER TABLE ph_collector_cpu ADD CONSTRAINT fkdbaf7cef88a1a383 FOREIGN KEY (collector_status_id)
      REFERENCES ph_collector_status (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_collector_disk ADD CONSTRAINT fk9a407b3688a1a383 FOREIGN KEY (collector_status_id)
      REFERENCES ph_collector_status (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_collector_disk_io ADD CONSTRAINT fk75c3a2cf88a1a383 FOREIGN KEY (collector_status_id)
      REFERENCES ph_collector_status (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_collector_mem_swap ADD CONSTRAINT fkb257ad688a1a383 FOREIGN KEY (collector_status_id)
      REFERENCES ph_collector_status (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_event_parser ADD CONSTRAINT fkcdbd544b41f1e972 FOREIGN KEY (device_type_id)
      REFERENCES ph_device_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_event_parser ADD CONSTRAINT fkcdbd544b656115d6 FOREIGN KEY (prev_parser_id)
      REFERENCES ph_event_parser (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_notification_action ADD CONSTRAINT fk15241343db07a067 FOREIGN KEY (notification_policy_id)
      REFERENCES ph_notification_policy (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_notification_condition ADD CONSTRAINT fkf1f6a0eedb07a067 FOREIGN KEY (notification_policy_id)
      REFERENCES ph_notification_policy (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_perf_transform ADD CONSTRAINT fkd6f3babd241fc2f1 FOREIGN KEY (oid_id)
      REFERENCES ph_mon_oid (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_dev_ip_hostname ADD CONSTRAINT fk60f33ada94ed2ae5 FOREIGN KEY (device_id)
      REFERENCES ph_device (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_cust_property ADD CONSTRAINT fk2154c43af9a19405 FOREIGN KEY (property_def_id)
      REFERENCES ph_cust_property_def (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

--
-- add index
--


--
-- drop constraints
--

--
-- new sequence
--
-- Sequence: ph_event_attr_type_id_gen

-- DROP SEQUENCE ph_event_attr_type_id_gen;

CREATE SEQUENCE ph_event_attr_type_id_gen
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 59999
  START 10000
  CACHE 1;
ALTER TABLE ph_event_attr_type_id_gen OWNER TO phoenix;

--
-- data migration
--

CREATE OR REPLACE FUNCTION current_epoch_time() RETURNS bigint AS $$
DECLARE
   epochtime real;
   currenttime bigint;
BEGIN
  SELECT extract(epoch FROM now()) into epochtime;
  currenttime := ceil(epochtime) * 1000;
  return currenttime;
END
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION ph_migrate_notification() RETURNS integer AS $$
DECLARE
   nview RECORD;
   dview RECORD;
   nextid bigint;
   currenttime bigint;
   naturalid character varying(255);
   actiontype character varying(255);
   actiondefinition text;
   displayorder integer;
   actionorder integer;
   custid bigint;
BEGIN
  displayorder := 0;
  select current_epoch_time() INTO currenttime;
  FOR nview IN SELECT id, cust_org_id, event_source_id, "name" FROM ph_notification WHERE event_source_type='Rule' LOOP
    displayorder := displayorder + 1;
    IF nview.cust_org_id = 0 THEN
        custid := 3;
    ELSE
        custid := nview.cust_org_id;
    END IF;
    nextid := nextval('ph_global_gen');
    insert into ph_notification_policy (id, creation_time, cust_org_id, last_modified_time, owner_id, entity_version, display_order, enabled, "name") values (nextid, currenttime, custid, currenttime, 0, 0, displayorder, true, nview.name);
    IF nview.name !='Default for all rules' AND nview.event_source_id > 0 THEN
       select natural_id into naturalid from ph_drq_rule where id=nview.event_source_id;
       insert into ph_notification_condition (id, creation_time, cust_org_id, last_modified_time, owner_id, included, condition_name, condition_type, notification_policy_id, display_order) values (nextval('ph_global_gen'), currenttime, custid, currenttime, 0, true, naturalid, 'RULE', nextid, 0);
    END IF;
    actionorder := -1;
      FOR dview IN SELECT receipt, receipt_type, "type" from ph_delivery where notification_id= nview.id LOOP
          actionorder := actionorder + 1;
	  IF dview.receipt_type = 'VALUE' THEN
              IF dview.type = 'EMAIL' THEN
              	actiontype := 'Email';
                actiondefinition := dview.receipt;
              ELSEIF dview.type = 'SMS' THEN
                actiontype := 'SMS';
                actiondefinition := dview.receipt;
              ELSEIF dview.type = 'ALERT' THEN
                actiontype := 'Alert';
                actiondefinition := '';
              END IF;
          ELSEIF dview.receipt_type = 'HTTP' THEN
              actiontype := 'HTTP';
              actiondefinition := '';
          ELSEIF dview.receipt_type = 'HTTPS' THEN
              actiontype := 'HTTPS';
              actiondefinition := '';
          ELSEIF dview.receipt_type = 'SNMP' THEN
              actiontype := 'SNMPTrap';
              actiondefinition := '';
          END IF;
               
          insert into ph_notification_action (id, creation_time, cust_org_id, last_modified_time, owner_id, action_definition, action_type, notification_policy_id, display_order) values (nextval('ph_global_gen'), currenttime, custid, currenttime, 0, actiondefinition, actiontype, nextid, actionorder);
      END LOOP;
  END LOOP;
  RETURN 0;
END
$$ LANGUAGE 'plpgsql';

select ph_migrate_notification();

CREATE OR REPLACE FUNCTION ph_migrate_collector_status() RETURNS integer AS $$
DECLARE
   cview RECORD;
   nextid bigint;
   currenttime bigint;
BEGIN
  select current_epoch_time() INTO currenttime;
  FOR cview IN SELECT c.cust_org_id AS custid, c."name" AS collectorname, c.collector_id AS collectorid, c.ip_addr AS addr, d."name" AS custname FROM ph_sys_collector c, ph_sys_domain d where c.cust_org_id=d.domain_id LOOP    
    nextid := nextval('ph_global_gen');
    insert into ph_collector_status (id, creation_time, cust_org_id, last_modified_time, owner_id, collector_id, collector_name, cust_name, ip_addr) values (nextid, currenttime, cview.custid, currenttime, 0, cview.collectorid, cview.collectorname, cview.custname, cview.addr);
  END LOOP;
  RETURN 0;
END
$$ LANGUAGE 'plpgsql';

select ph_migrate_collector_status();

DROP FUNCTION current_epoch_time();
DROP FUNCTION ph_migrate_notification();
DROP FUNCTION ph_migrate_collector_status();

--
-- update db version
--
update ph_sys_conf set value = '3.5.1' where property = 'DB_Schema_Version';
