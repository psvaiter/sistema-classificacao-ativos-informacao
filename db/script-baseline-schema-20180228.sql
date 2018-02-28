-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema db_information_asset_security
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_information_asset_security` DEFAULT CHARACTER SET utf8 ;
USE `db_information_asset_security` ;

-- -----------------------------------------------------
-- Table `db_information_asset_security`.`basic_classification_level`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`basic_classification_level` (
  `basic_classification_level_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`basic_classification_level_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`business_department`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`business_department` (
  `business_department_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`business_department_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`business_macroprocess`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`business_macroprocess` (
  `business_macroprocess_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`business_macroprocess_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`business_process`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`business_process` (
  `business_process_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`business_process_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`country`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`country` (
  `iso_31661_numeric` INT(11) NOT NULL,
  `iso_31661_alpha2` CHAR(2) NOT NULL,
  `iso_31661_alpha3` CHAR(3) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`iso_31661_numeric`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`country_subdivision`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`country_subdivision` (
  `country_subdivision_id` VARCHAR(6) NOT NULL,
  `country_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `external_identifier` VARCHAR(16) NULL DEFAULT NULL,
  PRIMARY KEY (`country_subdivision_id`),
  INDEX `IX_country_id` (`country_id` ASC),
  CONSTRAINT `FK_country_subdivision_country`
    FOREIGN KEY (`country_id`)
    REFERENCES `db_information_asset_security`.`country` (`iso_31661_numeric`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`it_asset`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`it_asset` (
  `it_asset_id` INT(11) NOT NULL AUTO_INCREMENT,
  `it_asset_category_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`it_asset_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC),
  INDEX `IX_it_asset_category_id` (`it_asset_category_id` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`it_asset_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`it_asset_category` (
  `it_asset_category_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`it_asset_category_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`it_service`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`it_service` (
  `it_service_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`it_service_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`organization`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization` (
  `organization_id` INT(11) NOT NULL AUTO_INCREMENT,
  `tax_id` VARCHAR(16) NOT NULL,
  `legal_name` VARCHAR(128) NOT NULL,
  `trade_name` VARCHAR(128) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`organization_business_department`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization_business_department` (
  `organization_business_department_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `business_department_id` INT(11) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_business_department_id`),
  UNIQUE INDEX `UQ_organization_id_department_id` (`organization_id` ASC, `business_department_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  INDEX `IX_business_department_id` (`business_department_id` ASC),
  CONSTRAINT `FK_org_biz_department_business_department`
    FOREIGN KEY (`business_department_id`)
    REFERENCES `db_information_asset_security`.`business_department` (`business_department_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_biz_department_organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `db_information_asset_security`.`organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`organization_business_macroprocess`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization_business_macroprocess` (
  `organization_business_macroprocess_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `business_department_id` INT(11) NOT NULL,
  `business_macroprocess_id` INT(11) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_business_macroprocess_id`),
  UNIQUE INDEX `UQ_organization_id_department_id_macroprocess_id` (`organization_id` ASC, `business_department_id` ASC, `business_macroprocess_id` ASC),
  INDEX `IX_business_department_id` (`business_department_id` ASC),
  INDEX `IX_business_macroprocess_id` (`business_macroprocess_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  CONSTRAINT `FK_org_biz_macroprocess_business_department`
    FOREIGN KEY (`business_department_id`)
    REFERENCES `db_information_asset_security`.`business_department` (`business_department_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_biz_macroprocess_business_macroprocess`
    FOREIGN KEY (`business_macroprocess_id`)
    REFERENCES `db_information_asset_security`.`business_macroprocess` (`business_macroprocess_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_biz_macroprocess_organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `db_information_asset_security`.`organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`organization_business_process`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization_business_process` (
  `organization_business_process_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `business_macroprocess_id` INT(11) NOT NULL,
  `business_process_id` INT(11) NOT NULL,
  `relevance_level_id` INT(11) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_business_process_id`),
  UNIQUE INDEX `UQ_organization_id_macroprocess_id_process_id` (`organization_id` ASC, `business_macroprocess_id` ASC, `business_process_id` ASC),
  INDEX `IX_business_macroprocess_id` (`business_macroprocess_id` ASC),
  INDEX `IX_business_process_id` (`business_process_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  INDEX `IX_basic_classification_level_id` (`relevance_level_id` ASC),
  CONSTRAINT `FK_org_biz_process_basic_classification_level`
    FOREIGN KEY (`relevance_level_id`)
    REFERENCES `db_information_asset_security`.`basic_classification_level` (`basic_classification_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_biz_process_business_macroprocess`
    FOREIGN KEY (`business_macroprocess_id`)
    REFERENCES `db_information_asset_security`.`business_macroprocess` (`business_macroprocess_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_biz_process_business_process`
    FOREIGN KEY (`business_process_id`)
    REFERENCES `db_information_asset_security`.`business_process` (`business_process_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_biz_process_organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `db_information_asset_security`.`organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`organization_it_asset`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization_it_asset` (
  `organization_it_asset_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `it_service_id` INT(11) NOT NULL,
  `it_asset_id` INT(11) NOT NULL,
  `relevance_level_id` INT(11) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_it_asset_id`),
  UNIQUE INDEX `UQ_organization_id_information_service_id_information_asset_id` (`organization_id` ASC, `it_service_id` ASC, `it_asset_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  INDEX `IX_basic_classification_level_id` (`relevance_level_id` ASC),
  INDEX `IX_it_service_id` (`it_service_id` ASC),
  INDEX `IX_it_asset_id` (`it_asset_id` ASC),
  CONSTRAINT `FK_org_it_asset_basic_classification_level`
    FOREIGN KEY (`relevance_level_id`)
    REFERENCES `db_information_asset_security`.`basic_classification_level` (`basic_classification_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_it_asset_information_asset`
    FOREIGN KEY (`it_asset_id`)
    REFERENCES `db_information_asset_security`.`it_asset` (`it_asset_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_it_asset_information_service`
    FOREIGN KEY (`it_service_id`)
    REFERENCES `db_information_asset_security`.`it_service` (`it_service_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_it_asset_organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `db_information_asset_security`.`organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`security_threat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`security_threat` (
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
-- Table `db_information_asset_security`.`organization_it_asset_vulnerability`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization_it_asset_vulnerability` (
  `organization_it_asset_vulnerability_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `security_threat_id` INT(11) NOT NULL,
  `information_asset_id` INT(11) NOT NULL,
  `vulnerability_level_id` INT(11) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_it_asset_vulnerability_id`),
  UNIQUE INDEX `UQ_organization_id_information_asset_id_security_threat_id` (`organization_id` ASC, `information_asset_id` ASC, `security_threat_id` ASC),
  INDEX `IX_information_asset_id` (`information_asset_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  INDEX `IX_security_threat_id` (`security_threat_id` ASC),
  INDEX `IX_basic_classification_level_id` (`vulnerability_level_id` ASC),
  CONSTRAINT `FK_org_info_asset_vulnerability_basic_classification_level`
    FOREIGN KEY (`vulnerability_level_id`)
    REFERENCES `db_information_asset_security`.`basic_classification_level` (`basic_classification_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_info_asset_vulnerability_information_asset`
    FOREIGN KEY (`information_asset_id`)
    REFERENCES `db_information_asset_security`.`it_asset` (`it_asset_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_info_asset_vulnerability_organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `db_information_asset_security`.`organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_info_asset_vulnerability_security_threat`
    FOREIGN KEY (`security_threat_id`)
    REFERENCES `db_information_asset_security`.`security_threat` (`security_threat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`organization_it_service`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization_it_service` (
  `organization_it_service_id` INT(11) NOT NULL,
  `organization_id` INT(11) NOT NULL,
  `business_process_id` INT(11) NOT NULL,
  `it_service_id` INT(11) NOT NULL,
  `relevance_level_id` INT(11) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_it_service_id`),
  UNIQUE INDEX `UQ_organization_id_process_id_information_service_id` (`organization_id` ASC, `business_process_id` ASC, `it_service_id` ASC),
  INDEX `IX_business_process_id` (`business_process_id` ASC),
  INDEX `IX_basic_classification_level_id` (`relevance_level_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  INDEX `IX_it_service_id` (`it_service_id` ASC),
  CONSTRAINT `FK_org_it_service_basic_classification_level`
    FOREIGN KEY (`relevance_level_id`)
    REFERENCES `db_information_asset_security`.`basic_classification_level` (`basic_classification_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_it_service_business_process`
    FOREIGN KEY (`business_process_id`)
    REFERENCES `db_information_asset_security`.`business_process` (`business_process_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_it_service_information_service`
    FOREIGN KEY (`it_service_id`)
    REFERENCES `db_information_asset_security`.`it_service` (`it_service_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_it_service_organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `db_information_asset_security`.`organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`organization_location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization_location` (
  `organization_location_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_id` INT(11) NOT NULL,
  `latitude` DECIMAL(9,6) NULL DEFAULT NULL,
  `longitude` DECIMAL(9,6) NULL DEFAULT NULL,
  `postal_code` VARCHAR(16) NULL DEFAULT NULL,
  `country_subdivision_id` VARCHAR(6) NULL DEFAULT NULL,
  `city_name` VARCHAR(128) NULL DEFAULT NULL,
  `street_address_1` VARCHAR(128) NULL DEFAULT NULL,
  `street_address_2` VARCHAR(128) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_location_id`),
  INDEX `IX_organization_id` (`organization_id` ASC),
  INDEX `IX_country_subdivision_id` (`country_subdivision_id` ASC),
  CONSTRAINT `FK_org_location_country_subdivision`
    FOREIGN KEY (`country_subdivision_id`)
    REFERENCES `db_information_asset_security`.`country_subdivision` (`country_subdivision_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_location_organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `db_information_asset_security`.`organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`organization_security_threat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization_security_threat` (
  `organization_security_threat_id` INT(11) NOT NULL,
  `organization_id` INT(11) NOT NULL,
  `security_threat_id` INT(11) NOT NULL,
  `exposure_level_id` INT(11) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`organization_security_threat_id`),
  UNIQUE INDEX `UQ_organization_id_security_threat_id` (`organization_id` ASC, `security_threat_id` ASC),
  INDEX `IX_organization_id` (`organization_id` ASC),
  INDEX `IX_security_threat_id` (`security_threat_id` ASC),
  INDEX `IX_basic_classification_level_id` (`exposure_level_id` ASC),
  CONSTRAINT `FK_org_security_threat_basic_classification_level`
    FOREIGN KEY (`exposure_level_id`)
    REFERENCES `db_information_asset_security`.`basic_classification_level` (`basic_classification_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_security_threat_organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `db_information_asset_security`.`organization` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_security_threat_security_threat`
    FOREIGN KEY (`security_threat_id`)
    REFERENCES `db_information_asset_security`.`security_threat` (`security_threat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`organization_vulnerability_control`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`organization_vulnerability_control` (
  `organization_vulnerability_control_id` INT(11) NOT NULL AUTO_INCREMENT,
  `organization_it_asset_id` INT(11) NOT NULL,
  `controller_it_asset_id` INT(11) NULL DEFAULT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`organization_vulnerability_control_id`),
  INDEX `FK_org_vulnerability_control_org_it_asset_idx` (`organization_it_asset_id` ASC),
  INDEX `FK_org_vulnerability_control_it_asset_idx` (`controller_it_asset_id` ASC),
  CONSTRAINT `FK_org_vulnerability_control_it_asset`
    FOREIGN KEY (`controller_it_asset_id`)
    REFERENCES `db_information_asset_security`.`organization_it_asset` (`organization_it_asset_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_org_vulnerability_control_org_it_asset`
    FOREIGN KEY (`organization_it_asset_id`)
    REFERENCES `db_information_asset_security`.`organization_it_asset` (`organization_it_asset_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`system_administrative_role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`system_administrative_role` (
  `system_administrative_role_id` INT(11) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`system_administrative_role_id`),
  UNIQUE INDEX `UQ_name` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`system_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`system_user` (
  `system_user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(128) NOT NULL,
  `password` VARCHAR(32) NULL DEFAULT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  `last_logged_in_on` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`system_user_id`),
  UNIQUE INDEX `UQ_email` (`email` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `db_information_asset_security`.`system_user_administrative_role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_information_asset_security`.`system_user_administrative_role` (
  `system_user_administrative_role_id` INT(11) NOT NULL AUTO_INCREMENT,
  `system_user_id` INT(11) NOT NULL,
  `system_administrative_role_id` INT(11) NOT NULL,
  `created_on` DATETIME(3) NOT NULL,
  `last_modified_on` DATETIME(3) NOT NULL,
  PRIMARY KEY (`system_user_administrative_role_id`),
  UNIQUE INDEX `UQ_system_user_administrative_role` (`system_user_id` ASC, `system_administrative_role_id` ASC),
  INDEX `IX_user_role_system_user` (`system_user_id` ASC),
  INDEX `IX_user_role_system_administrative_role` (`system_administrative_role_id` ASC),
  CONSTRAINT `FK_user_role_system_administrative_role`
    FOREIGN KEY (`system_administrative_role_id`)
    REFERENCES `db_information_asset_security`.`system_administrative_role` (`system_administrative_role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_user_role_system_user`
    FOREIGN KEY (`system_user_id`)
    REFERENCES `db_information_asset_security`.`system_user` (`system_user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
