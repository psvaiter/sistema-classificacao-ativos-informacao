-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema knoweak
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `knoweak` DEFAULT CHARACTER SET utf8;
USE `knoweak`;


-- -----------------------------------------------------
-- Table `business_department`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `business_department` (
  `business_department_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`business_department_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `business_macroprocess`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `business_macroprocess` (
  `business_macroprocess_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`business_macroprocess_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `business_process`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `business_process` (
  `business_process_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`business_process_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `it_asset_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `it_asset_category` (
  `it_asset_category_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`it_asset_category_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `it_asset`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `it_asset` (
  `it_asset_id` INT(11) NOT NULL AUTO_INCREMENT,
  `it_asset_category_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`it_asset_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC),
  INDEX `IX_it_asset_category_id` (`it_asset_category_id` ASC),
  CONSTRAINT `FK_it_asset__it_asset_category`
    FOREIGN KEY (`it_asset_category_id`)
    REFERENCES `it_asset_category` (`it_asset_category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `it_service`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `it_service` (
  `it_service_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`it_service_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mitigation_control`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mitigation_control` (
  `mitigation_control_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`mitigation_control_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization` (
  `organization_id` INT(11) NOT NULL AUTO_INCREMENT,
  `tax_id` VARCHAR(16) NOT NULL,
  `legal_name` VARCHAR(128) NOT NULL,
  `trade_name` VARCHAR(128) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_id`),
  UNIQUE INDEX `UQ_taxi_id_legal_name_trade_name` (`tax_id` ASC, `legal_name` ASC, `trade_name` ASC),
  INDEX `IX_tax_id` (`tax_id` ASC),
  INDEX `IX_legal_name` (`legal_name` ASC),
  INDEX `IX_trade_name` (`trade_name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_analysis`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_analysis` (
  `organization_analysis_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `description` VARCHAR(1024) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_analysis_id`),
  INDEX `IX_organization_id` (`organization_id` ASC),
  CONSTRAINT `FK_organization_analysis__organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_analysis_detail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_analysis_detail` (
  `organization_analysis_detail_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_analysis_id` INT(11) NOT NULL,
  `department_name` VARCHAR(128) NOT NULL,
  `macroprocess_name` VARCHAR(128) NOT NULL,
  `process_name` VARCHAR(128) NOT NULL,
  `process_relevance` INT(11) NOT NULL,
  `it_service_name` VARCHAR(128) NOT NULL,
  `it_service_relevance` INT(11) NOT NULL,
  `it_asset_name` VARCHAR(128) NOT NULL,
  `it_asset_relevance` INT(11) NOT NULL,
  `calculated_impact` DECIMAL(5,4) NOT NULL,
  `security_threat_name` VARCHAR(128) NOT NULL,
  `security_threat_level` INT(11) NOT NULL,
  `it_asset_vulnerability_level` INT(11) NOT NULL,
  `calculated_probability` DECIMAL(5,4) NOT NULL,
  `calculated_risk` DECIMAL(5,4) NOT NULL,
  PRIMARY KEY (`organization_analysis_detail_id`),
  INDEX `IX_organization_analysis_id` (`organization_analysis_id` ASC),
  CONSTRAINT `FK_organization_analysis_detail__organization_analysis`
    FOREIGN KEY (`organization_analysis_id`)
    REFERENCES `organization_analysis` (`organization_analysis_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_department`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_department` (
  `organization_id` INT(11) NOT NULL,
  `business_department_id` INT(11) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_id`, `business_department_id`),
  INDEX `IX_organization_id` (`organization_id` ASC),
  INDEX `IX_business_department_id` (`business_department_id` ASC),
  CONSTRAINT `FK_organization_department__business_department`
    FOREIGN KEY (`business_department_id`)
    REFERENCES `business_department` (`business_department_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_department__organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `organization` (`organization_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_it_asset`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_it_asset` (
  `organization_it_asset_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `it_asset_id` INT(11) NOT NULL,
  `external_identifier` VARCHAR(128) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_it_asset_id`),
  INDEX `IX_it_asset_id` (`it_asset_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  CONSTRAINT `FK_organization_it_asset__it_asset`
    FOREIGN KEY (`it_asset_id`)
    REFERENCES `it_asset` (`it_asset_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_it_asset__organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `organization` (`organization_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_it_asset_control`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_it_asset_control` (
  `organization_it_asset_control_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_it_asset_id` INT(11) NOT NULL,
  `mitigation_control_id` INT(11) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_it_asset_control_id`),
  INDEX `IX_mitigation_control_id` (`mitigation_control_id` ASC),
  INDEX `IX_organization_it_asset_id` (`organization_it_asset_id` ASC),
  CONSTRAINT `FK_organization_it_asset_control__mitigation_control`
    FOREIGN KEY (`mitigation_control_id`)
    REFERENCES `mitigation_control` (`mitigation_control_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_it_asset_control__organization_it_asset`
    FOREIGN KEY (`organization_it_asset_id`)
    REFERENCES `organization_it_asset` (`organization_it_asset_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `rating_level`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rating_level` (
  `rating_level_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`rating_level_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `security_threat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `security_threat` (
  `security_threat_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`security_threat_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_security_threat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_security_threat` (
  `organization_security_threat_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `security_threat_id` INT(11) NOT NULL,
  `threat_level_id` INT(11) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_security_threat_id`),
  UNIQUE INDEX `UQ_organization_id_security_threat_id` (`organization_id` ASC, `security_threat_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  INDEX `IX_security_threat_id` (`security_threat_id` ASC),
  INDEX `IX_threat_level_id` (`threat_level_id` ASC),
  CONSTRAINT `FK_organization_security_threat__organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `organization` (`organization_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_security_threat__rating_level`
    FOREIGN KEY (`threat_level_id`)
    REFERENCES `rating_level` (`rating_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_security_threat__security_threat`
    FOREIGN KEY (`security_threat_id`)
    REFERENCES `security_threat` (`security_threat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_it_asset_vulnerability`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_it_asset_vulnerability` (
  `organization_it_asset_vulnerability_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_security_threat_id` INT(11) NOT NULL,
  `organization_it_asset_id` INT(11) NOT NULL,
  `vulnerability_level_id` INT(11) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_it_asset_vulnerability_id`),
  INDEX `IX_organization_it_asset_id` (`organization_it_asset_id` ASC),
  INDEX `IX_vulnerability_level_id` (`vulnerability_level_id` ASC),
  INDEX `IX_organization_security_threat_id` (`organization_security_threat_id` ASC),
  CONSTRAINT `FK_organization_it_asset_vulnerability__organization_it_asset`
    FOREIGN KEY (`organization_it_asset_id`)
    REFERENCES `organization_it_asset` (`organization_it_asset_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_it_asset_vulnerability__organization_sec_threat`
    FOREIGN KEY (`organization_security_threat_id`)
    REFERENCES `organization_security_threat` (`organization_security_threat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_it_asset_vulnerability__rating_level`
    FOREIGN KEY (`vulnerability_level_id`)
    REFERENCES `rating_level` (`rating_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_macroprocess`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_macroprocess` (
  `organization_macroprocess_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `business_department_id` INT(11) NOT NULL,
  `business_macroprocess_id` INT(11) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_macroprocess_id`),
  INDEX `IX_business_macroprocess_id` (`business_macroprocess_id` ASC),
  INDEX `IX_organization_department_id` (`organization_id` ASC, `business_department_id` ASC),
  CONSTRAINT `FK_organization_macroprocess__business_macroprocess`
    FOREIGN KEY (`business_macroprocess_id`)
    REFERENCES `business_macroprocess` (`business_macroprocess_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_macroprocess__organization_department`
    FOREIGN KEY (`organization_id` , `business_department_id`)
    REFERENCES `organization_department` (`organization_id` , `business_department_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_process`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_process` (
  `organization_process_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `organization_macroprocess_id` INT(11) NOT NULL,
  `business_process_id` INT(11) NOT NULL,
  `relevance_level_id` INT(11) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_process_id`),
  INDEX `IX_business_process_id` (`business_process_id` ASC),
  INDEX `IX_relevance_level_id` (`relevance_level_id` ASC),
  INDEX `IX_organization_macroprocess_id` (`organization_macroprocess_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  CONSTRAINT `FK_organization_process__basic_classification_level`
    FOREIGN KEY (`relevance_level_id`)
    REFERENCES `rating_level` (`rating_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_process__business_process`
    FOREIGN KEY (`business_process_id`)
    REFERENCES `business_process` (`business_process_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_process__organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_process__organization_macroprocess`
    FOREIGN KEY (`organization_macroprocess_id`)
    REFERENCES `organization_macroprocess` (`organization_macroprocess_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_it_service`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_it_service` (
  `organization_it_service_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `organization_process_id` INT(11) NOT NULL,
  `it_service_id` INT(11) NOT NULL,
  `relevance_level_id` INT(11) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_it_service_id`),
  INDEX `IX_it_service_id` (`it_service_id` ASC),
  INDEX `IX_relevance_level_id` (`relevance_level_id` ASC),
  INDEX `IX_organization_process_id` (`organization_process_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  CONSTRAINT `FK_organization_it_service__it_service`
    FOREIGN KEY (`it_service_id`)
    REFERENCES `it_service` (`it_service_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_it_service__organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_it_service__organization_process`
    FOREIGN KEY (`organization_process_id`)
    REFERENCES `organization_process` (`organization_process_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_it_service__rating_level`
    FOREIGN KEY (`relevance_level_id`)
    REFERENCES `rating_level` (`rating_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `organization_it_service_it_asset`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `organization_it_service_it_asset` (
  `organization_it_service_id` INT(11) NOT NULL,
  `organization_it_asset_id` INT(11) NOT NULL,
  `relevance_level_id` INT(11) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_it_service_id`, `organization_it_asset_id`),
  INDEX `IX_organization_it_service_id` (`organization_it_service_id` ASC),
  INDEX `IX_organization_it_asset_id` (`organization_it_asset_id` ASC),
  INDEX `IX_rating_level_id` (`relevance_level_id` ASC),
  CONSTRAINT `FK_organization_it_service_it_asset__organization_it_asset`
    FOREIGN KEY (`organization_it_asset_id`)
    REFERENCES `organization_it_asset` (`organization_it_asset_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_it_service_it_asset__organization_it_service`
    FOREIGN KEY (`organization_it_service_id`)
    REFERENCES `organization_it_service` (`organization_it_service_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_organization_it_service_it_asset__rating_level`
    FOREIGN KEY (`relevance_level_id`)
    REFERENCES `rating_level` (`rating_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `system_permission`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `system_permission` (
  `system_permission_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`system_permission_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `system_role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `system_role` (
  `system_role_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`system_role_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `system_role_permission`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `system_role_permission` (
  `system_role_id` INT(11) NOT NULL,
  `system_permission_id` INT(11) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`system_role_id`, `system_permission_id`),
  INDEX `IX_system_permission_id` (`system_permission_id` ASC),
  CONSTRAINT `FK_system_role_permission__system_permission`
    FOREIGN KEY (`system_permission_id`)
    REFERENCES `system_permission` (`system_permission_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_system_role_permission__system_role`
    FOREIGN KEY (`system_role_id`)
    REFERENCES `system_role` (`system_role_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `system_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `system_user` (
  `system_user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(128) NOT NULL,
  `hashed_password` VARBINARY(64) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  `locked_out_on` DATETIME(3) NULL DEFAULT NULL,
  `blocked_on` DATETIME(3) NULL DEFAULT NULL,
  PRIMARY KEY (`system_user_id`),
  UNIQUE INDEX `UQ_email` (`email` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `system_user_login`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `system_user_login` (
  `system_user_login_id` INT(11) NOT NULL AUTO_INCREMENT,
  `system_user_id` INT(11) NOT NULL,
  `attempted_on` DATETIME(3) NOT NULL,
  `was_successful` BIT(1) NOT NULL,
  PRIMARY KEY (`system_user_login_id`),
  INDEX `IX_system_user_id` (`system_user_id` ASC),
  CONSTRAINT `FK_system_user_login__system_user`
    FOREIGN KEY (`system_user_id`)
    REFERENCES `system_user` (`system_user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `system_user_permission`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `system_user_permission` (
  `system_user_id` INT(11) NOT NULL,
  `system_permission_id` INT(11) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`system_user_id`, `system_permission_id`),
  INDEX `IX_system_permission_id` (`system_permission_id` ASC),
  CONSTRAINT `FK_system_user_permission__system_permission`
    FOREIGN KEY (`system_permission_id`)
    REFERENCES `system_permission` (`system_permission_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_system_user_permission__system_user`
    FOREIGN KEY (`system_user_id`)
    REFERENCES `system_user` (`system_user_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `system_user_role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `system_user_role` (
  `system_user_id` INT(11) NOT NULL,
  `system_role_id` INT(11) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`system_user_id`, `system_role_id`),
  INDEX `IX_system_role_id` (`system_role_id` ASC),
  CONSTRAINT `FK_system_user_role__system_role`
    FOREIGN KEY (`system_role_id`)
    REFERENCES `system_role` (`system_role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_system_user_role__system_user`
    FOREIGN KEY (`system_user_id`)
    REFERENCES `system_user` (`system_user_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
