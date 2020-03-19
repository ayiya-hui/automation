\set ON_ERROR_STOP on

--
-- new table
--

--
-- new colums
--
alter table ph_drq_rule add column change_type integer;
alter table ph_drq_rule add column creation_type integer;
alter table ph_drq_report add column creation_type integer;
alter table ph_rbac_profile add column creation_type integer;
alter table ph_rbac_profile add column natural_id character varying(255);
alter table ph_sys_collector add column ip_addr character varying(255);

--
-- constraints
--

--
-- add index
--

CREATE INDEX ph_contact_email_index ON ph_contact USING btree (email);
create index ph_user2contact_user_id_key on ph_user2contact (user_id);
create index ph_user_domain_mapping_user_id_key on ph_user_domain_mapping (user_id);
create index ph_user_domain_profile_mapping_user_id_key on ph_user_domain_profile_mapping (user_id);
CREATE INDEX ph_uc_ucid_only_index ON ph_user_id_loc USING btree (uc_id);


--
-- drop constraints
--

--
-- data migration
--
--

-- update ph_schedule set user_id for report
--
update ph_schedule set user_id=owner_id where (owner_id > 0) and (user_id =0 or user_id is null) and job_data_type='Report';

update ph_schedule set user_id = (select id from ph_user where cust_org_id=0 and name='admin') where cust_org_id=3;

CREATE OR REPLACE FUNCTION ph_up_schedule_user_id() RETURNS integer AS $$
DECLARE
   scheduleview RECORD;
   userid bigint;
BEGIN
  FOR scheduleview IN SELECT id, cust_org_id FROM ph_schedule WHERE (user_id=0 or user_id is null) and (owner_id is null or owner_id=0) and job_data_type='Report' LOOP
      select u.id INTO userid from ph_user u, ph_rbac_profile p where u.prime_profile_id=p.id and p.name='Full Admin' and u.cust_org_id=scheduleview.cust_org_id limit 1;
      UPDATE ph_schedule SET user_id = userid
                             WHERE id = scheduleview.id;
  END LOOP;
  RETURN 0;
END
$$ LANGUAGE 'plpgsql';

select ph_up_schedule_user_id();

--
-- update ph_drq_report_inst set owner_id = admin id
--

CREATE OR REPLACE FUNCTION ph_up_report_inst_owner_id() RETURNS integer AS $$
DECLARE
   instanceview RECORD;
   userid bigint;
BEGIN
  FOR instanceview IN SELECT id, cust_org_id FROM ph_drq_report_inst WHERE owner_id is null or owner_id=0 LOOP
      select u.id INTO userid from ph_user u, ph_rbac_profile p where u.prime_profile_id=p.id and p.name='Full Admin' and u.cust_org_id=instanceview.cust_org_id limit 1;
      UPDATE ph_drq_report_inst SET owner_id = userid
                             WHERE id = instanceview.id;
  END LOOP;
  RETURN 0;
END
$$ LANGUAGE 'plpgsql';

select ph_up_report_inst_owner_id();

--
-- update db version
--
update ph_sys_conf set value = '3.1.2' where property = 'DB_Schema_Version';
