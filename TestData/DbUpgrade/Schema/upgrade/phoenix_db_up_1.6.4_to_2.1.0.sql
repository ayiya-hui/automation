\set ON_ERROR_STOP on

--
-- Tables
--
-- Table: ph_impacted_cust

-- DROP TABLE ph_impacted_cust;

CREATE TABLE ph_impacted_cust
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  device_id bigint NOT NULL,
  impacted_cust_id bigint NOT NULL,
  collector_id bigint,
  CONSTRAINT ph_impacted_cust_pkey PRIMARY KEY (id),
  CONSTRAINT ph_impacted_cust_device_id FOREIGN KEY (device_id)
      REFERENCES ph_device (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT ph_impacted_cust_id FOREIGN KEY (impacted_cust_id)
      REFERENCES ph_sys_domain (domain_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITHOUT OIDS;
ALTER TABLE ph_impacted_cust OWNER TO phoenix;

-- Table: ph_disc_ip_range

-- DROP TABLE ph_disc_ip_range;

CREATE TABLE ph_disc_ip_range
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  exclude_range text,
  include_range text,
  last_discovery_time bigint,
  "name" character varying(255),
  root_ip text,
  CONSTRAINT ph_disc_ip_range_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_disc_ip_range OWNER TO phoenix;

-- Table: ph_incident

-- DROP TABLE ph_incident;

CREATE TABLE ph_incident
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  biz_service text,
  incident_cache_index text,
  cleared_reason text,
  cleared_time bigint,
  cleared_user character varying(255),
  comments text,
  first_seen_time bigint,
  incident_count integer,
  incident_detail text,
  incident_et text,
  incident_id bigint,
  incident_src text,
  incident_status integer,
  incident_target text,
  last_seen_time bigint,
  notif_recipients text,
  rule_id bigint,
  severity integer,
  severity_cat character varying(255),
  ticket_id character varying(2048),
  ticket_status integer,
  view_status integer,
  view_users character varying(255),
  ticket_user character varying(1024),
  orig_device_ip character varying(255),
  cleared_events text,
  CONSTRAINT ph_incident_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_incident OWNER TO phoenix;


-- Table: ph_incident_detail

-- DROP TABLE ph_incident_detail;

CREATE TABLE ph_incident_detail
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  duration bigint,
  incident_detail text,
  incident_id bigint,
  incident_timestamp bigint,
  notif_recipients text,
  trigger_events text,
  CONSTRAINT ph_incident_detail_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_incident_detail OWNER TO phoenix;

-- Table: ph_country_restriction

-- DROP TABLE ph_country_restriction;

CREATE TABLE ph_country_restriction
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  country character varying(255),
  res_type integer,
  res_value character varying(1024),
  CONSTRAINT ph_country_restriction_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_country_restriction OWNER TO phoenix;

-- Table: ph_critical_intf

-- DROP TABLE ph_critical_intf;

CREATE TABLE ph_critical_intf
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  device_name character varying(512),
  intf_name character varying(512),
  access_ip character varying(255),
  CONSTRAINT ph_critical_intf_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_critical_intf OWNER TO phoenix;

-- Table: ph_filter_ip_app

-- DROP TABLE ph_filter_ip_app;

CREATE TABLE ph_filter_ip_app
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  app_name text,
  app_para text,
  app_path text,
  excluded boolean NOT NULL,
  CONSTRAINT ph_filter_ip_app_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_filter_ip_app OWNER TO phoenix;

-- DROP TABLE ph_saved_port;

CREATE TABLE ph_saved_port
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  port_num character varying(255),
  port_type character varying(255),
  CONSTRAINT ph_saved_port_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_saved_port OWNER TO phoenix;

-- Table: ph_drq_clear_condition

-- DROP TABLE ph_drq_clear_condition;

CREATE TABLE ph_drq_clear_condition
(
  id bigint NOT NULL,
  collector_id bigint,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  clear_constraints text,
  clear_filter_operator character varying(2048),
  clear_global_constraints text,
  clear_incident_attrs text,
  clear_incident_name character varying(255),
  clear_option character varying(255),
  clear_time_window integer,
  rule_id bigint,
  rule_natural_id character varying(255),
  CONSTRAINT ph_drq_clear_condition_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_drq_clear_condition OWNER TO phoenix;

-- Table: ph_drq_clear_condition2event_filter

-- DROP TABLE ph_drq_clear_condition2event_filter;

CREATE TABLE ph_drq_clear_condition2event_filter
(
  clear_condition_id bigint NOT NULL,
  event_filter_id bigint NOT NULL,
  CONSTRAINT fk5885b5698ed21932 FOREIGN KEY (clear_condition_id)
      REFERENCES ph_drq_clear_condition (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk5885b569d092eafc FOREIGN KEY (event_filter_id)
      REFERENCES ph_drq_filter (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT ph_drq_clear_condition2event_filter_event_filter_id_key UNIQUE (event_filter_id)
)
WITHOUT OIDS;
ALTER TABLE ph_drq_clear_condition2event_filter OWNER TO phoenix;

-- Table: ph_topo_edge

-- DROP TABLE ph_topo_edge

CREATE TABLE ph_topo_edge
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  node1_id bigint,
  node2_id bigint,
  param text,
  collector_id bigint,
  layer integer,
  CONSTRAINT ph_topo_edge_pkey PRIMARY KEY (id),
  CONSTRAINT ph_topo_edge_node1_id_fkey FOREIGN KEY (node1_id)
      REFERENCES ph_topo_node (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT ph_topo_edge_node2_id_fkey FOREIGN KEY (node2_id)
      REFERENCES ph_topo_node (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITHOUT OIDS;
ALTER TABLE ph_topo_edge OWNER TO phoenix;

-- Table: ph_topo_graph2topo_edge

-- DROP TABLE ph_topo_graph2topo_edge;

CREATE TABLE ph_topo_graph2topo_edge
(
  topo_graph_id bigint NOT NULL,
  topo_edge_id bigint NOT NULL,
  CONSTRAINT ph_topo_graph2topo_edge_pkey PRIMARY KEY (topo_graph_id, topo_edge_id),
  CONSTRAINT ph_topo_graph2topo_edge_topo_edge_id_key UNIQUE (topo_edge_id),
  CONSTRAINT ph_topo_graph2topo_edge_topo_graph_id_fkey FOREIGN KEY (topo_graph_id)
      REFERENCES ph_topo_graph (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT ph_topo_graph2topo_edge_topo_edge_id_fkey FOREIGN KEY (topo_edge_id)
      REFERENCES ph_topo_edge (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITHOUT OIDS;
ALTER TABLE ph_topo_graph2topo_edge OWNER TO phoenix;

--
-- Add columns
--

--
-- ph_domain
--
ALTER TABLE ph_sys_domain ADD COLUMN exclude_range text;
ALTER TABLE ph_sys_domain ADD COLUMN include_range text;
ALTER TABLE ph_sys_domain ADD COLUMN address character varying(2048);
ALTER TABLE ph_sys_domain ADD COLUMN phone character varying(255);
ALTER TABLE ph_sys_domain ADD COLUMN collector_id bigint;


--
-- ph_sys_collector
--
ALTER TABLE ph_sys_collector ADD COLUMN start_time bigint;
ALTER TABLE ph_sys_collector ADD COLUMN end_time bigint;
ALTER TABLE ph_sys_collector ADD COLUMN eps integer NOT NULL;
ALTER TABLE ph_sys_collector ADD COLUMN registered boolean;
ALTER TABLE ph_sys_collector ADD COLUMN collector_id bigint;

--
--ph_device
--
ALTER TABLE ph_sys_collector ADD CONSTRAINT "ph_sys_collector_agentId" UNIQUE(agent_id);
ALTER TABLE ph_device ADD COLUMN collector_id bigint;
ALTER TABLE ph_device ADD COLUMN service_tag character varying(255);
ALTER TABLE ph_device ADD COLUMN os_edition character varying(1024);
ALTER TABLE ph_device
  ADD CONSTRAINT "ph_device2ph_sys_collector_agentId" FOREIGN KEY (collector_id)
      REFERENCES ph_sys_collector (agent_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

--
--ph_monitor_config
--
ALTER TABLE ph_monitor_config ADD COLUMN collector_id bigint;
ALTER TABLE ph_monitor_config ADD COLUMN target character varying(512);

--
--ph_drq_rule
--
ALTER TABLE ph_drq_rule ADD COLUMN collector_id bigint;
ALTER TABLE ph_drq_rule ADD COLUMN fire_internal_incident boolean;

--
--ph_device_ep_access
--
ALTER TABLE ph_device_ep_access ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_ep_access ADD COLUMN target character varying(512);
--
--Add collector_id columns
--
ALTER TABLE ph_agent_status ADD COLUMN collector_id bigint;
ALTER TABLE ph_alert ADD COLUMN collector_id bigint;
ALTER TABLE ph_app ADD COLUMN collector_id bigint;
ALTER TABLE ph_app_pkg ADD COLUMN collector_id bigint;
ALTER TABLE ph_biz_svc ADD COLUMN collector_id bigint;
ALTER TABLE ph_biz_svc_item ADD COLUMN collector_id bigint;
ALTER TABLE ph_change_set ADD COLUMN collector_id bigint;
ALTER TABLE ph_contact ADD COLUMN collector_id bigint;
ALTER TABLE ph_dashboard ADD COLUMN collector_id bigint;
ALTER TABLE ph_dbd_widget ADD COLUMN collector_id bigint;
ALTER TABLE ph_delivery ADD COLUMN collector_id bigint;
ALTER TABLE ph_dev_event_attr ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_access ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_access_mapping ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_comp ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_credential ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_intf ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_patch ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_proc ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_storage ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_sw_svc ADD COLUMN collector_id bigint;
ALTER TABLE ph_device_type ADD COLUMN collector_id bigint;
ALTER TABLE ph_disc_profile ADD COLUMN collector_id bigint;
ALTER TABLE ph_drq_cust_activation ADD COLUMN collector_id bigint;
ALTER TABLE ph_drq_filter ADD COLUMN collector_id bigint;
ALTER TABLE ph_drq_metrics ADD COLUMN collector_id bigint;
ALTER TABLE ph_drq_report ADD COLUMN collector_id bigint;
ALTER TABLE ph_drq_report_inst ADD COLUMN collector_id bigint;
ALTER TABLE ph_drq_rule_exp ADD COLUMN collector_id bigint;
ALTER TABLE ph_drq_scope ADD COLUMN collector_id bigint;
ALTER TABLE ph_eo_props ADD COLUMN collector_id bigint;
ALTER TABLE ph_event_attr_type ADD COLUMN collector_id bigint;
ALTER TABLE ph_event_code ADD COLUMN collector_id bigint;
ALTER TABLE ph_event_type ADD COLUMN collector_id bigint;
ALTER TABLE ph_filter_ip_range ADD COLUMN collector_id bigint;
ALTER TABLE ph_group ADD COLUMN collector_id bigint;
ALTER TABLE ph_group_item ADD COLUMN collector_id bigint;
ALTER TABLE ph_incident_ticket ADD COLUMN collector_id bigint;
ALTER TABLE ph_incident_ticket_trail ADD COLUMN collector_id bigint;
ALTER TABLE ph_ip_access_mapping ADD COLUMN collector_id bigint;
ALTER TABLE ph_layer2_conn ADD COLUMN collector_id bigint;
ALTER TABLE ph_malware_site ADD COLUMN collector_id bigint;
ALTER TABLE ph_managed_mapping ADD COLUMN collector_id bigint;
ALTER TABLE ph_mon_oid ADD COLUMN collector_id bigint;
ALTER TABLE ph_mon_perf_obj ADD COLUMN collector_id bigint;
ALTER TABLE ph_mon_template ADD COLUMN collector_id bigint;
ALTER TABLE ph_mon_template_item ADD COLUMN collector_id bigint;
ALTER TABLE ph_monitee ADD COLUMN collector_id bigint;
ALTER TABLE ph_monitor_type ADD COLUMN collector_id bigint;
ALTER TABLE ph_network ADD COLUMN collector_id bigint;
ALTER TABLE ph_net_service ADD COLUMN collector_id bigint;
ALTER TABLE ph_notification ADD COLUMN collector_id bigint;
ALTER TABLE ph_schedule ADD COLUMN collector_id bigint;
ALTER TABLE ph_sec_ident ADD COLUMN collector_id bigint;
ALTER TABLE ph_sec_locked_client ADD COLUMN collector_id bigint;
ALTER TABLE ph_sec_login_trail ADD COLUMN collector_id bigint;
ALTER TABLE ph_sec_privilege ADD COLUMN collector_id bigint;
ALTER TABLE ph_sec_role ADD COLUMN collector_id bigint;
ALTER TABLE ph_sec_session_trail ADD COLUMN collector_id bigint;
ALTER TABLE ph_svc_mon ADD COLUMN collector_id bigint;
ALTER TABLE ph_svc_probe ADD COLUMN collector_id bigint;
ALTER TABLE ph_svc_probe_ss ADD COLUMN collector_id bigint;
ALTER TABLE ph_sys_collector_trail ADD COLUMN collector_id bigint;
ALTER TABLE ph_sys_conf ADD COLUMN collector_id bigint;
ALTER TABLE ph_sys_cust_res ADD COLUMN collector_id bigint;
ALTER TABLE ph_sys_cust_res_usage ADD COLUMN collector_id bigint;
ALTER TABLE ph_sys_data_repos ADD COLUMN collector_id bigint;
ALTER TABLE ph_sys_server ADD COLUMN collector_id bigint;
ALTER TABLE ph_task ADD COLUMN collector_id bigint;
ALTER TABLE ph_tmp_id_map ADD COLUMN collector_id bigint;
ALTER TABLE ph_topo_graph ADD COLUMN collector_id bigint;
ALTER TABLE ph_topo_node ADD COLUMN collector_id bigint;
ALTER TABLE ph_topo_node ADD COLUMN layer integer;
ALTER TABLE ph_user ADD COLUMN collector_id bigint;
ALTER TABLE ph_user_id_loc ADD COLUMN collector_id bigint;
ALTER TABLE ph_vul ADD COLUMN collector_id bigint;
ALTER TABLE ph_vul_sw ADD COLUMN collector_id bigint;
ALTER TABLE ph_incident_ticket ADD COLUMN assignee_name character varying(512);

--
-- drop index
--

--
-- add index
--
CREATE INDEX ph_incident_incidentid_index ON ph_incident USING btree (incident_id);
CREATE INDEX ph_incident_custid_index ON ph_incident USING btree (cust_org_id);
CREATE INDEX ph_incident_lastseen_index ON ph_incident USING btree (last_seen_time);
CREATE INDEX ph_incident_detail_custid_index ON ph_incident_detail (cust_org_id);
CREATE INDEX ph_incident_detail_incidentid_index ON ph_incident_detail (incident_id);

CREATE INDEX device_accessip_null_idx ON ph_device USING btree (access_ip) WHERE collector_id IS NULL;
CREATE INDEX device_hwserialno_null_idx ON ph_device USING btree (hw_serial_no) WHERE collector_id IS NULL;
CREATE INDEX device_name_null_idx ON ph_device USING btree (lower(name)) WHERE collector_id IS NULL;

CREATE INDEX app_name_null_idx ON ph_app USING btree (lower(name)) WHERE collector_id IS NULL;

CREATE INDEX ninf_ipv4addr_null_idx ON ph_device_intf USING btree (ipv4_addr) WHERE collector_id IS NULL;
CREATE INDEX ninf_macaddr_null_idx ON ph_device_intf USING btree (mac_addr) WHERE collector_id IS NULL;

CREATE INDEX task_status_null_idx ON ph_task USING btree (status) WHERE collector_id IS NULL;

CREATE INDEX ipaccessmapping_iprange_null_idx ON ph_ip_access_mapping USING btree (ip_range) WHERE collector_id IS NULL;

CREATE INDEX ph_uc_lseen_index ON ph_user_id_loc USING btree (last_seen_time) WHERE switch_name IS NOT NULL AND host_name IS NOT NULL;
CREATE INDEX ph_uc_lseenip_index ON ph_user_id_loc USING btree (last_seen_time) WHERE switch_name IS NOT NULL AND host_name IS NULL AND ip_addr IS NOT NULL;
CREATE INDEX ph_uc_swhn_index ON ph_user_id_loc USING btree (switch_name, host_name) WHERE switch_name IS NOT NULL AND host_name IS NOT NULL;
CREATE INDEX ph_uc_swip_index ON ph_user_id_loc USING btree (switch_name, ip_addr) WHERE switch_name IS NOT NULL AND ip_addr IS NOT NULL;

--
-- data migration
--
Update ph_monitor_config set target = (select access_ip from ph_device where id = device_id) where data_type = 1;
Update ph_monitor_config set device_id = null where data_type = 1;

insert into ph_disc_ip_range (id, creation_time, cust_org_id, last_modified_time, owner_id, entity_version, exclude_range, include_range, "name") 
	select id, creation_time, cust_org_id, last_modified_time, owner_id, entity_version, exclude_range, include_range, split_part(include_range, ',', 1) || '-' || nextval('ph_global_gen') from ph_access_ip_range;

insert into ph_disc_ip_range (id, creation_time, cust_org_id, last_modified_time, owner_id, entity_version, exclude_range, include_range, "name", root_ip) 
	select id, creation_time, cust_org_id, last_modified_time, owner_id, entity_version, exclude_list, include_list, split_part(root_ip, ',', 1) || '-' || nextval('ph_global_gen'), root_ip from ph_disc_profile where root_ip is not null order by last_modified_time DESC LIMIT 1;

--
-- drop columns
-- drop tables/columns
--

drop table ph_access_ip_range;

drop table ph_topo_node2topo_node;

drop table ph_topo_graph2topo_node;

delete from ph_topo_node;

--
-- new sequence
--
-- Sequence: ph_domain_id_gen

-- DROP SEQUENCE ph_domain_id_gen;

CREATE SEQUENCE ph_domain_id_gen
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 2000
  CACHE 1;
ALTER TABLE ph_domain_id_gen OWNER TO phoenix;

-- Sequence: ph_collector_id_gen

-- DROP SEQUENCE ph_collector_id_gen;

CREATE SEQUENCE ph_collector_id_gen
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 10000
  CACHE 1;
ALTER TABLE ph_collector_id_gen OWNER TO phoenix;

-- Sequence: ph_incident_id_gen

-- DROP SEQUENCE ph_incident_id_gen;

CREATE SEQUENCE ph_incident_id_gen 
  INCREMENT 100
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE ph_incident_id_gen  OWNER TO phoenix;

--
-- update db version
--
update ph_sys_conf set value = '2.1.0' where property = 'DB_Schema_Version';
