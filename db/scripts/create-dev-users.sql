-- Create dev user
CREATE USER 'developer'@'%' IDENTIFIED BY 'dev-pass';
GRANT ALL PRIVILEGES ON *.* TO 'developer'@'%';

-- Create application user
CREATE USER 'KnoweakAppUser'@'%' IDENTIFIED BY 'app_pass';
GRANT SELECT, INSERT, UPDATE, DELETE ON knoweak.* TO 'KnoweakAppUser'@'%';