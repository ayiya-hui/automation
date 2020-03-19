\set ON_ERROR_STOP on

ALTER TABLE ph_cm_cust_lic ADD COLUMN num_of_org integer;
ALTER TABLE ph_cm_cust_lic ADD COLUMN sp boolean;
ALTER TABLE ph_cm_cust_lic ADD COLUMN country character varying(255);