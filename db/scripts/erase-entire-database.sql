-- Erase organizations
delete from organization_analysis where organization_analysis_id > 0;
delete from organization where organization_id > 0;

-- Erase catalog
delete from business_department where business_department_id > 0;
delete from business_macroprocess where business_macroprocess_id > 0;
delete from business_process where business_process_id > 0;
delete from it_service where it_service_id > 0;
delete from it_asset where it_asset_id > 0;
delete from security_threat where security_threat_id > 0;
delete from mitigation_control where mitigation_control_id > 0;

-- Erase seed data
delete from it_asset_category where it_asset_category_id > 0;
delete from rating_level where rating_level_id > 0;
