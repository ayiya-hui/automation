\set ON_ERROR_STOP on

--
-- Tables
--

-- Table: ph_access_ip_range

CREATE TABLE ph_access_ip_range
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  exclude_range character varying(255),
  include_range character varying(255),
  CONSTRAINT ph_access_ip_range_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_access_ip_range OWNER TO phoenix;

-- Table: ph_dev_event_attr

CREATE TABLE ph_dev_event_attr
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  attrnamelist character varying(4096),
  device_type_id bigint,
  event_type_id bigint,
  CONSTRAINT ph_dev_event_attr_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_dev_event_attr OWNER TO phoenix;


-- Table: ph_device_access_mapping

CREATE TABLE ph_device_access_mapping
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  access_method_id bigint,
  device_id bigint,
  CONSTRAINT ph_device_access_mapping_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_device_access_mapping OWNER TO phoenix;

ALTER TABLE ph_device_access RENAME TO ph_device_access_old;
ALTER TABLE ph_device_credential RENAME TO ph_device_credential_old;
ALTER TABLE ph_device_access_old DROP CONSTRAINT ph_device_access_pkey cascade;
ALTER TABLE ph_device_credential_old DROP CONSTRAINT ph_device_credential_pkey cascade;

CREATE TABLE ph_device_access
(
  id bigint NOT NULL,
  creation_time bigint default 0,
  cust_org_id bigint,
  entity_version bigint default 0,
  last_modified_time bigint default 0,
  owner_id bigint default 0,
  access_proto character varying(255),
  agent_id character varying(255),
  base_dn character varying(255),
  client_name character varying(255),
  description character varying(2048),
  "name" character varying(255),
  port integer NOT NULL,
  server_name character varying(255),
  transport character varying(255),
  credential_id bigint,
  device_type_id bigint,
  pull_interval integer,
  param character varying(4096),
  CONSTRAINT ph_device_access_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_device_access OWNER TO phoenix;


CREATE TABLE ph_device_credential
(
  id bigint NOT NULL,
  creation_time bigint default 0,
  cust_org_id bigint,
  entity_version bigint default 0,
  last_modified_time bigint default 0,
  owner_id bigint default 0,
  certificate text,
  "name" character varying(255),
  "password" character varying(255),
  principal character varying(255),
  su_password character varying(255),
  "type" integer,
  CONSTRAINT ph_device_credential_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_device_credential OWNER TO phoenix;


-- Table: ph_device_ep_access
CREATE TABLE ph_device_ep_access
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  enabled boolean NOT NULL,
  access_method_id bigint,
  device_id bigint,
  CONSTRAINT ph_device_ep_access_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_device_ep_access OWNER TO phoenix;

-- Table: ph_device_patch
CREATE TABLE ph_device_patch
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  description character varying(2048),
  install_time bigint,
  installed_by character varying(255),
  "name" character varying(255),
  device_id bigint,
  CONSTRAINT ph_device_patch_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_device_patch OWNER TO phoenix;

-- Table: ph_device_sw_svc
CREATE TABLE ph_device_sw_svc
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  description character varying(2048),
  display_name character varying(255),
  "name" character varying(255),
  exec_path character varying(255),
  start_mode character varying(255),
  started_flag boolean,
  running_state character varying(255),
  status character varying(255),
  device_id bigint,
  CONSTRAINT ph_device_sw_svc_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_device_sw_svc OWNER TO phoenix;


-- Table: ph_drq_cust_activation

CREATE TABLE ph_drq_cust_activation
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  data_request_id bigint,
  activated_time bigint,
  customer_id bigint,
  CONSTRAINT ph_drq_cust_activation_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_drq_cust_activation OWNER TO phoenix;

-- Table: ph_drq_rule_exp
CREATE TABLE ph_drq_rule_exp
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  single_constr text,
  rule_id bigint,
  rule_natural_id character varying(255),
  time_expr character varying(255),
  CONSTRAINT ph_drq_rule_exp_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_drq_rule_exp OWNER TO phoenix;


-- Table: ph_incident_ticket
CREATE TABLE ph_incident_ticket
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  assignee_id bigint,
  creator character varying(255),
  due_date date,
  expire_time bigint,
  incident_sid character varying(255),
  observers character varying(2048),
  priority integer NOT NULL,
  remark character varying(2048),
  ticket_state integer,
  CONSTRAINT ph_incident_ticket_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_incident_ticket OWNER TO phoenix;

-- Table: ph_incident_ticket_trail
CREATE TABLE ph_incident_ticket_trail
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  "action" character varying(255),
  "comment" text,
  obj character varying(255),
  subject character varying(255),
  ticket_id bigint,
  CONSTRAINT ph_incident_ticket_trail_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_incident_ticket_trail OWNER TO phoenix;

-- Table: ph_ip_access_mapping
CREATE TABLE ph_ip_access_mapping
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  access_method_id bigint,
  ip_range character varying(255),
  CONSTRAINT ph_ip_access_mapping_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_ip_access_mapping OWNER TO phoenix;


-- Table: ph_malware_site
CREATE TABLE ph_malware_site
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  description character varying(255),
  domain_name character varying(255),
  CONSTRAINT ph_malware_site_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_malware_site OWNER TO phoenix;

-- Table: ph_monitor_config
CREATE TABLE ph_monitor_config
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  enabled boolean NOT NULL,
  device_id bigint,
  perf_object_id bigint,
  CONSTRAINT ph_monitor_config_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_monitor_config OWNER TO phoenix;

-- Table: ph_monitor_type
CREATE TABLE ph_monitor_type
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  entity_version bigint,
  category character varying(255),
  description character varying(255),
  displayname character varying(255),
  "name" character varying(255),
  CONSTRAINT ph_monitor_type_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_monitor_type OWNER TO phoenix;

-- Table: ph_sec_locked_client

-- DROP TABLE ph_sec_locked_client;

CREATE TABLE ph_sec_locked_client
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  domain_id bigint,
  remote_addr character varying(255),
  user_id bigint,
  CONSTRAINT ph_sec_locked_client_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_sec_locked_client OWNER TO phoenix;

-- Table: ph_sec_login_trail
CREATE TABLE ph_sec_login_trail
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  attemp_failed boolean,
  domain_id bigint,
  remote_addr character varying(255),
  user_id bigint,
  CONSTRAINT ph_sec_login_trail_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_sec_login_trail OWNER TO phoenix;

-- Table: ph_sec_session_trail
CREATE TABLE ph_sec_session_trail
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  client_addr character varying(255),
  latest_request_time bigint,
  login_id character varying(255),
  request_count integer,
  server_addr character varying(255),
  session_id character varying(255),
  session_state integer,
  CONSTRAINT ph_sec_session_trail_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_sec_session_trail OWNER TO phoenix;


-- Table: ph_vul
CREATE TABLE ph_vul
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  bug_id character varying(255),
  cve_code character varying(255),
  description character varying(2048),
  vendor_bug_id character varying(255),
  CONSTRAINT ph_vul_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_vul OWNER TO phoenix;

-- Table: ph_vul_ph_event_type
CREATE TABLE ph_vul2event_type
(
  vul_id bigint NOT NULL,
  event_type_id bigint NOT NULL
)
WITHOUT OIDS;
ALTER TABLE ph_vul2event_type OWNER TO phoenix;

-- Table: ph_vul_sw
CREATE TABLE ph_vul_sw
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  app_model character varying(2048),
  app_vendor character varying(2048),
  app_version character varying(2048),
  fix_date date,
  fix_ver character varying(255),
  os_version character varying(2048),
  patch_id character varying(2048),
  os_device_type_id bigint,
  vul_id bigint,
  CONSTRAINT ph_vul_sw_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_vul_sw OWNER TO phoenix;

--
-- alter tables  Add columns
--
ALTER TABLE ph_app ADD COLUMN sw_services character varying(255);
ALTER TABLE ph_app ADD COLUMN up_time integer;
ALTER TABLE ph_app ALTER COLUMN proc_name type character varying(2048);
ALTER TABLE ph_app ALTER COLUMN name type character varying(511);
ALTER TABLE ph_app ALTER COLUMN natural_id type character varying(511);
ALTER TABLE ph_app_pkg ADD COLUMN natural_id character varying(511);

ALTER TABLE ph_device ADD COLUMN natural_id character varying(255);
ALTER TABLE ph_device ADD COLUMN bios_name character varying(255);
ALTER TABLE ph_device ADD COLUMN bios_serialno character varying(255);
ALTER TABLE ph_device ADD COLUMN bios_vendor character varying(255);
ALTER TABLE ph_device ADD COLUMN bios_version character varying(255);
ALTER TABLE ph_device ADD COLUMN build_number character varying(255);
ALTER TABLE ph_device ADD COLUMN os_serial_no character varying(255);
ALTER TABLE ph_device ADD COLUMN perf_mon_enabled boolean default true;
ALTER TABLE ph_device ADD COLUMN event_pulling_enabled boolean default true;

-- ALTER TABLE ph_device_access ADD COLUMN description character varying(2048);
-- ALTER TABLE ph_device_access ADD COLUMN "name" character varying(255);
-- ALTER TABLE ph_device_access ADD COLUMN credential_id bigint;

ALTER TABLE ph_device_proc ADD COLUMN addr_width integer;
ALTER TABLE ph_device_proc ADD COLUMN cpu_util integer;
ALTER TABLE ph_device_proc ADD COLUMN curr_clock_speed integer;
ALTER TABLE ph_device_proc ADD COLUMN data_width integer;
ALTER TABLE ph_device_proc ADD COLUMN l2_cache_size integer;
ALTER TABLE ph_device_proc ADD COLUMN l2_cache_speed integer;
ALTER TABLE ph_device_proc ADD COLUMN manufacturer character varying(255);
ALTER TABLE ph_device_proc ADD COLUMN max_clock_speed integer;
ALTER TABLE ph_device_proc ADD COLUMN "version" character varying(255);

ALTER TABLE ph_device_type ADD COLUMN access_protos character varying(255);
ALTER TABLE ph_device_type ADD COLUMN event_parsed boolean;
ALTER TABLE ph_device_type ADD COLUMN priority int;

ALTER TABLE ph_drq_report ADD COLUMN category integer;
ALTER TABLE ph_drq_rule ADD COLUMN category integer;
ALTER TABLE ph_drq_rule ADD COLUMN advanced boolean;

ALTER TABLE ph_malware_site ADD COLUMN natural_id character varying(255);

ALTER TABLE ph_mon_perf_obj ADD COLUMN mon_type_id bigint;
ALTER TABLE ph_mon_perf_obj ADD COLUMN frequency integer;
ALTER TABLE ph_mon_perf_obj ADD COLUMN threshold integer;

ALTER TABLE ph_mon_template_item ALTER COLUMN frequency DROP NOT NULL;
ALTER TABLE ph_mon_template_item ALTER COLUMN threshold DROP NOT NULL;

ALTER TABLE ph_monitor_config ADD COLUMN effective_method character varying(255);

ALTER TABLE ph_net_service ADD COLUMN natural_id character varying(255);

ALTER TABLE ph_network ADD COLUMN high character varying(255);
ALTER TABLE ph_network ADD COLUMN low character varying(255);
ALTER TABLE ph_network ADD COLUMN natural_id character varying(255);

ALTER TABLE ph_sys_cust_res ADD COLUMN end_time bigint;
ALTER TABLE ph_sys_cust_res ADD COLUMN start_time bigint;
ALTER TABLE ph_sys_cust_res ADD COLUMN duration integer;
ALTER TABLE ph_sys_cust_res ADD COLUMN registered boolean;

ALTER TABLE ph_sys_domain ADD COLUMN disabled boolean;

ALTER TABLE ph_user ADD COLUMN natural_id character varying(255);

CREATE OR REPLACE FUNCTION inet_aton(text) RETURNS bigint AS '
SELECT
split_part($1,''.'',1)::int8*(256*256*256)+
split_part($1,''.'',2)::int8*(256*256)+
split_part($1,''.'',3)::int8*256+
split_part($1,''.'',4)::int8;
' LANGUAGE 'SQL';

CREATE OR REPLACE FUNCTION inet_ntoa(bigint) RETURNS text AS '
SELECT (($1>>24) & 255::int8) || ''.'' ||
(($1>>16) & 255::int8) || ''.'' ||
(($1>>8) & 255::int8) || ''.'' ||
($1 & 255::int8) as result
'
LANGUAGE 'SQL';

CREATE TABLE ph_tmp_am_index
(
  cust_org_id bigint,
  index int
)
WITHOUT OIDS;
ALTER TABLE ph_tmp_am_index OWNER TO phoenix;

CREATE OR REPLACE FUNCTION ph_up_dev_access() RETURNS integer AS $$
DECLARE
   amindex int;
   credid bigint;
   amid bigint;
   daview RECORD;
BEGIN
  FOR daview IN SELECT * FROM ph_device_access_old a inner join ph_device_access2credential b
              on a.id = b.access_method_id inner join ph_device_credential_old c on b.credential_id = c.id LOOP
    -- new credential
    credid := nextval('ph_global_gen');
    INSERT INTO ph_device_credential (id, creation_time, cust_org_id, entity_version, last_modified_time, owner_id, password, principal, su_password, type)
    VALUES  (credid, daview.creation_time, daview.cust_org_id, daview.entity_version, daview.last_modified_time, daview.owner_id,
                     daview.password, daview.principal, daview.su_password, daview.type);
    -- new access method
    amid := nextval('ph_global_gen');
    -- get am name index
    SELECT index INTO amindex FROM ph_tmp_am_index WHERE cust_org_id = daview.cust_org_id;
    IF amindex IS NULL THEN
       amindex := 1;
       INSERT INTO ph_tmp_am_index (cust_org_id, index) VALUES (daview.cust_org_id, 2);
    ELSE
       UPDATE ph_tmp_am_index SET index = index + 1 WHERE cust_org_id = daview.cust_org_id;
    END IF;

    INSERT INTO ph_device_access (id, creation_time, cust_org_id, entity_version, last_modified_time, owner_id, name, access_proto,
                    agent_id, base_dn, client_name, port, server_name, transport, device_type_id, pull_interval, param, credential_id)
    VALUES (amid, daview.creation_time, daview.cust_org_id, daview.entity_version, daview.last_modified_time, 
                    daview.owner_id, 'AM_' || amindex || '_' || daview.access_proto, daview.access_proto, daview.agent_id, daview.base_dn,
                    daview.client_name, daview.port, daview.server_name, daview.transport, daview.device_type_id, daview.pull_interval, daview.param, credid);

    -- device access mapping
    IF daview.device_id IS NOT NULL THEN
        INSERT INTO ph_device_access_mapping (id, creation_time, cust_org_id, entity_version, last_modified_time, owner_id, access_method_id, device_id)
        VALUES (nextval('ph_global_gen'), daview.creation_time, daview.cust_org_id, daview.entity_version, daview.last_modified_time, daview.owner_id, amid, daview.device_id);
        IF daview.used_by_flag & 4 > 0 THEN
            INSERT INTO ph_device_ep_access (id, creation_time, cust_org_id, entity_version, last_modified_time, owner_id, access_method_id, device_id, enabled)
            VALUES (nextval('ph_global_gen'), daview.creation_time, daview.cust_org_id, daview.entity_version, daview.last_modified_time, daview.owner_id, amid, daview.device_id, true);
        END IF;
    ELSIF daview.access_ip IS NOT NULL THEN
        INSERT INTO ph_ip_access_mapping (id, creation_time, cust_org_id, entity_version, last_modified_time, owner_id, access_method_id, ip_range)
        VALUES (nextval('ph_global_gen'), daview.creation_time, daview.cust_org_id, daview.entity_version, daview.last_modified_time, daview.owner_id, amid, daview.access_ip);
        IF daview.used_by_flag & 1 > 0 THEN
            SELECT id INTO amid FROM ph_access_ip_range WHERE cust_org_id = daview.cust_org_id AND include_range = daview.access_ip;
            IF NOT FOUND THEN
                 INSERT INTO ph_access_ip_range (id, creation_time, cust_org_id, entity_version, last_modified_time, owner_id, include_range, exclude_range)
                 VALUES (nextval('ph_global_gen'), daview.creation_time, daview.cust_org_id, daview.entity_version, daview.last_modified_time, daview.owner_id, daview.access_ip, '');
            END IF;
        END IF;
    END IF;
    -- ip access mapping
  END LOOP;
  RETURN 0;
END
$$ LANGUAGE 'plpgsql';


CREATE OR REPLACE FUNCTION ph_up_natural_id_encode(text) RETURNS text AS $$
DECLARE
   index int;
   instr text;
   len int;
   ch text;
   enc text;
BEGIN
   instr := $1;
   len := char_length(instr);
   enc := '';
   IF len > 0 THEN
       FOR index IN 1..len LOOP
         ch := substr(instr, index, 1);
         IF (ch > 'Z' OR ch < 'A') AND (ch > 'z' OR ch < 'a') AND (ch > '9' OR ch < '0') AND ch <> '_' AND ch <> '.' AND ch <> '/' THEN
            ch := '%' || to_hex(ascii(ch));
         END IF;
         enc := enc || ch;
       END LOOP;
   END IF;
   RETURN enc;
END
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION ph_up_drq_cust_activation() RETURNS integer AS $$
DECLARE
   drqview RECORD;
   custview RECORD;
   tmpid bigint;
BEGIN
  FOR custview IN SELECT domain_id FROM ph_sys_domain WHERE domain_id > 100 LOOP
      FOR drqview IN SELECT id, inline_drq_no, activated_time FROM ph_drq_report
                     WHERE active = true AND inline = TRUE and cust_inclusive = true AND inline_drq_no IS NOT NULL LOOP
          SELECT id INTO tmpid FROM ph_drq_cust_activation WHERE data_request_id = drqview.id AND customer_id = custview.domain_id;
          IF NOT FOUND THEN
              INSERT INTO ph_drq_cust_activation (id, creation_time, cust_org_id, last_modified_time, owner_id, data_request_id, activated_time, customer_id)
              VALUES (nextval('ph_global_gen'), 0, 0, 0, 0, drqview.id, drqview.activated_time, custview.domain_id);
          END IF;
      END LOOP;
      FOR drqview IN SELECT a.id, a.inline_drq_no, a.activated_time FROM ph_drq_report a INNER JOIN ph_drq_scope b ON a.id = b.data_request_id
                     WHERE a.active = true AND a.inline = true AND a.cust_inclusive = false AND a.inline_drq_no IS NOT NULL AND b.customer_id = custview.domain_id LOOP
          SELECT id INTO tmpid FROM ph_drq_cust_activation WHERE data_request_id = drqview.id AND customer_id = custview.domain_id;
          IF NOT FOUND THEN
              INSERT INTO ph_drq_cust_activation (id, creation_time, cust_org_id, last_modified_time, owner_id, data_request_id, activated_time, customer_id)
              VALUES (nextval('ph_global_gen'), 0, 0, 0, 0, drqview.id, drqview.activated_time, custview.domain_id);
          END IF;
      END LOOP;
  END LOOP;
  RETURN 0;
END
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION ph_up_cust_res() RETURNS integer AS $$
DECLARE
   custview RECORD;
   tmpid bigint;
BEGIN
  FOR custview IN SELECT cust_org_id, last_modified_time FROM ph_sys_collector WHERE natural_id IS NOT NULL AND natural_id <> '' LOOP
      UPDATE ph_sys_cust_res SET start_time = custview.last_modified_time,
                                 duration = 365,
                                 end_time = custview.last_modified_time + 31536000000,
                                 registered = true
                             WHERE target_cust_id = custview.cust_org_id;
  END LOOP;
  RETURN 0;
END
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION ph_up_group_biz_svc() RETURNS integer AS $$
DECLARE
   gview RECORD;
   nextid bigint;
BEGIN
   nextid := nextval('ph_global_gen');
   insert into ph_group (id, creation_time, cust_org_id, entity_version, last_modified_time, owner_id, natural_id, name, display_name, type, value_type)
                 values (nextid, 0, 0, 0, 0, 0, 'PH_SYS_REPORT_BizSvc', 'PH_SYS_REPORT_BizSvc', 'Biz Service', 9, 1);
   FOR gview IN select * from ph_group where type = 9 and natural_id = 'PH_SYS_REPORT_BizSvc' and cust_org_id <> 0 LOOP
       UPDATE ph_group_item SET group_id = nextid WHERE group_id = gview.id;
       DELETE FROM ph_group WHERE id = gview.id;
   END LOOP;
   RETURN 0;
END
$$ LANGUAGE 'plpgsql';


--
-- execute data migration
--

update ph_network set low = ip_addr, high = inet_ntoa(inet_aton('255.255.255.255') - inet_aton(net_mask) + inet_aton(ip_addr));

-- update device access
select ph_up_dev_access();

-- create natural id
UPDATE ph_app_pkg SET natural_id = ph_up_natural_id_encode(name);
UPDATE ph_user SET natural_id = ph_up_natural_id_encode(name);
UPDATE ph_device SET natural_id = ph_up_natural_id_encode(name);
UPDATE ph_biz_svc SET natural_id = ph_up_natural_id_encode(name);
UPDATE ph_net_service SET natural_id = ph_up_natural_id_encode(name);
UPDATE ph_malware_site SET natural_id = ph_up_natural_id_encode(domain_name);

-- delete all old monitor performance data
TRUNCATE ph_mon_perf_obj, ph_mon_template, ph_mon_template2device_type, ph_mon_template_item, ph_monitee CASCADE;

-- per-cust activation time
select ph_up_drq_cust_activation();

UPDATE ph_device_type SET vendor = 'Generic' WHERE cust_org_id = 0 AND vendor = 'Unknown';

-- update cust resource
select ph_up_cust_res();

-- update old biz services' natural id

update ph_biz_svc set natural_id = 'PH_SYS_BizSrvc_Auth' where name = 'Auth Service';
update ph_biz_svc set natural_id = 'PH_SYS_BizSrvc_VPN' where name = 'VPN Service';
update ph_biz_svc set natural_id = 'PH_SYS_BizSrvc_FW' where name = 'Firewall Service';
update ph_biz_svc set natural_id = 'PH_SYS_BizSrvc_DNS' where name = 'DHCP/DNS Service';
update ph_biz_svc set natural_id = 'PH_SYS_BizSrvc_SecGw' where name = 'Security Gateway Service';
update ph_biz_svc set natural_id = 'PH_SYS_BizSrvc_PCI' where name = 'PCI Service';
update ph_biz_svc set natural_id = 'PH_SYS_BizSrvc_COBIT' where name = 'COBIT Service';

-- replace old biz service group
select ph_up_group_biz_svc();

--
-- Drop table / columns
--

DROP TABLE ph_tmp_am_index;

DROP FUNCTION ph_up_dev_access();

DROP TABLE ph_device_access_old;
DROP TABLE ph_device_credential_old;


-- ALTER TABLE ph_device_access DROP COLUMN device_id;
DROP TABLE ph_device_access2credential;

ALTER TABLE ph_mon_perf_obj DROP COLUMN "type";

ALTER TABLE ph_network DROP COLUMN ip_addr;
ALTER TABLE ph_network DROP COLUMN net_mask;
ALTER TABLE ph_alert DROP COLUMN create_time;
ALTER TABLE ph_task DROP COLUMN create_time;

--
-- Constraints
--

ALTER TABLE ph_dev_event_attr ADD CONSTRAINT ph_dev_event_attr2device_type_fk FOREIGN KEY (device_type_id)
      REFERENCES ph_device_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_dev_event_attr ADD CONSTRAINT ph_dev_event_attr2event_type_fk FOREIGN KEY (event_type_id)
      REFERENCES ph_event_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_device_access ADD CONSTRAINT ph_device_access2credential_fk FOREIGN KEY (credential_id)
      REFERENCES ph_device_credential (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_device_ep_access ADD CONSTRAINT ph_device_ep_access2device_access_fk FOREIGN KEY (access_method_id)
      REFERENCES ph_device_access (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_device_ep_access ADD CONSTRAINT ph_device_ep_access2device_fk FOREIGN KEY (device_id)
      REFERENCES ph_device (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_device_patch ADD CONSTRAINT ph_device_patch2device_fk FOREIGN KEY (device_id)
      REFERENCES ph_device (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_device_sw_svc ADD CONSTRAINT ph_device_sw_svc2device_fk FOREIGN KEY (device_id)
      REFERENCES ph_device (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_monitor_config ADD CONSTRAINT ph_monitor_config2mon_ferf_fk FOREIGN KEY (perf_object_id)
      REFERENCES ph_mon_perf_obj (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_monitor_config ADD CONSTRAINT ph_monitor_config2device_fk FOREIGN KEY (device_id)
      REFERENCES ph_device (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_incident_ticket_trail ADD CONSTRAINT ph_incident_ticket_trail2incident_ticket_fk FOREIGN KEY (ticket_id)
      REFERENCES ph_incident_ticket (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_mon_perf_obj ADD CONSTRAINT ph_mon_perf_obj2device_monitor_type_fk FOREIGN KEY (mon_type_id)
      REFERENCES ph_monitor_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

-- vulnerability

ALTER TABLE ph_vul2event_type ADD CONSTRAINT ph_vul_fk2event_type FOREIGN KEY (vul_id)
      REFERENCES ph_vul (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_vul2event_type ADD CONSTRAINT ph_vul2event_type_fk FOREIGN KEY (event_type_id)
      REFERENCES ph_event_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_vul_sw ADD CONSTRAINT ph_vul_sw2device_type_fk FOREIGN KEY (os_device_type_id)
      REFERENCES ph_device_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ph_vul_sw ADD CONSTRAINT ph_vul_sw2vul_fk FOREIGN KEY (vul_id)
      REFERENCES ph_vul (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;


-- 
-- index 
--

DROP INDEX ph_change_set_time_index;
DROP INDEX ph_eat_name_index;
DROP INDEX ph_event_type_name_index;
DROP INDEX ph_net_service_name_index;

CREATE INDEX ph_device_name_index ON ph_device (cust_org_id, name);
CREATE INDEX ph_eat_name_index ON ph_event_attr_type (cust_org_id, name);
CREATE INDEX ph_event_type_name_index ON ph_event_type (cust_org_id, name);
CREATE INDEX ph_net_service_name_index ON ph_net_service (cust_org_id, name);
CREATE INDEX ph_uc_ucid_ip_index ON ph_user_id_loc (cust_org_id, ip_addr);

--
-- data deletion
--

-- remove incorrect event type group mapping
delete from ph_group_item where item_id = (select id from ph_event_type where name = 'McAfee-EPO-1280');


--
-- update db version
--
update ph_sys_conf set value = '1.5.0' where property = 'DB_Schema_Version';
