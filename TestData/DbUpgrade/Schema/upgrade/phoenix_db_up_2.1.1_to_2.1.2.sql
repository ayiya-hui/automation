\set ON_ERROR_STOP on

CREATE INDEX ph_device_intf_devid_index ON ph_device_intf USING btree (device_id);
CREATE INDEX ph_biz_svc_bizsvcid_index ON ph_biz_svc_item USING btree (biz_svc_id);
CREATE INDEX ph_biz_svc_itemid_index ON ph_biz_svc_item USING btree (item_id);
CREATE INDEX ph_biz_svc_custid_index ON ph_biz_svc USING btree (cust_org_id);
CREATE INDEX ph_biz_svc_item_custid_index ON ph_biz_svc_item USING btree (cust_org_id);
alter table ph_impacted_cust add column update_method character varying(255);
--
-- update db version
--
update ph_sys_conf set value = '2.1.2' where property = 'DB_Schema_Version';
