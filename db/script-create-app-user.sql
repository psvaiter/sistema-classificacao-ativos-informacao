CREATE USER 'KnoweakAppUser'@'%' IDENTIFIED BY 'app_pass';
GRANT SELECT, INSERT, UPDATE, DELETE ON knoweak.* TO 'KnoweakAppUser'@'%';