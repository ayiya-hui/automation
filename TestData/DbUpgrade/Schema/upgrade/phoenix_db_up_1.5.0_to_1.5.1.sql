\set ON_ERROR_STOP on

--
-- Tables
--

-- Table: ph_filter_ip_range

CREATE TABLE ph_filter_ip_range
(
  id bigint NOT NULL,
  creation_time bigint default 0,
  cust_org_id bigint,
  entity_version bigint default 0,
  last_modified_time bigint default 0,
  owner_id bigint default 0,
  include_range character varying(2048),
  exclude_range character varying(2048),
  CONSTRAINT ph_filter_ip_range_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_filter_ip_range OWNER TO phoenix;

CREATE TABLE ph_sys_collector_trail
(
  id bigint NOT NULL,
  creation_time bigint,
  cust_org_id bigint,
  last_modified_time bigint,
  owner_id bigint,
  latest_request_time bigint,
  CONSTRAINT ph_sys_collector_trail_pkey PRIMARY KEY (id)
)
WITHOUT OIDS;
ALTER TABLE ph_sys_collector_trail OWNER TO phoenix;

ALTER TABLE ph_device_intf ADD COLUMN ipv4_is_virtual boolean;
ALTER TABLE ph_device_intf ADD COLUMN mac_is_virtual boolean;
ALTER TABLE ph_disc_profile ADD COLUMN virtual_ips text;
ALTER TABLE ph_sys_collector ADD COLUMN status boolean;

--
-- update db version
--
update ph_sys_conf set value = '1.5.1' where property = 'DB_Schema_Version';
