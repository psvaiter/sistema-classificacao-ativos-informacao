CREATE USER 'developer'@'%' IDENTIFIED BY 'dev-pass';
GRANT ALL PRIVILEGES ON *.* TO 'developer'@'%';

CREATE USER 'KnoweakAppUser'@'%' IDENTIFIED BY 'app_pass';
GRANT SELECT, INSERT, UPDATE, DELETE ON knoweak.* TO 'KnoweakAppUser'@'%';
