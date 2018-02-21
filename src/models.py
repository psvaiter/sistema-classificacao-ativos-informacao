from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dictalchemy import make_class_dictable
from datetime import datetime
from settings import conn_string

# Setup database connector
engine = create_engine(conn_string, echo=True)
Session = sessionmaker(bind=engine)

DbModel = declarative_base()
make_class_dictable(DbModel)


class Organization(DbModel):
    __tablename__ = "organization"

    organization_id = Column(Integer, primary_key=True)
    tax_id = Column(String, nullable=False)
    legal_name = Column(String, nullable=False)
    trade_name = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationLocation(DbModel):
    __tablename__ = "organization_location"

    organization_location_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.organization_id"))
    latitude = Column(Float)
    longitude = Column(Float)
    country_code = Column(String)
    country_subdivision_code = Column(String)
    postal_code = Column(String)
    city_name = Column(String)
    street_address_1 = Column(String)
    street_address_2 = Column(String)


class BusinessDepartment(DbModel):
    __tablename__ = "business_department"

    business_department_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class BusinessMacroprocess(DbModel):
    __tablename__ = "business_macroprocess"

    business_macroprocess_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class BusinessProcess(DbModel):
    __tablename__ = "business_process"

    business_process_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class ITService(DbModel):
    __tablename__ = "it_service"

    it_service_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class ITAsset(DbModel):
    __tablename__ = "it_asset"

    it_asset_id = Column(Integer, primary_key=True)
    category_id = Column("it_asset_category_id", Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Removed ForeignKey("it_asset_category.it_asset_category_id"),
    # from definition of category_id.


class ITAssetCategory(DbModel):
    __tablename__ = "it_asset_category"

    category_id = Column("it_asset_category_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class SecurityThreat(DbModel):
    __tablename__ = "security_threat"

    security_threat_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class SystemUser(DbModel):
    __tablename__ = "system_user"

    system_user_id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String)
    last_logged_in_on = Column(DateTime)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class SystemAdministrativeRole(DbModel):
    __tablename__ = "system_administrative_role"

    system_administrative_role_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class SystemUserAdministrativeRole(DbModel):
    __tablename__ = "system_user_administrative_role"

    system_user_administrative_role_id = Column(Integer, primary_key=True)
    system_user_id = Column(Integer, ForeignKey("system_user.system_user_id"), nullable=False)
    system_administrative_role_id = Column(Integer, ForeignKey("system_administrative_role.system_administrative_role_id"), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class BasicClassificationLevel(DbModel):
    __tablename__ = "basic_classification_level"

    basic_classification_level_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationDepartment(DbModel):
    __tablename__ = "organization_business_department"

    organization_business_department_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.organization_id"), nullable=False)
    business_department_id = Column(Integer, ForeignKey("business_department.business_department_id"), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationMacroprocess(DbModel):
    __tablename__ = "organization_business_macroprocess"

    organization_business_macroprocess_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.organization_id"), nullable=False)
    business_department_id = Column(Integer, ForeignKey("business_department.business_department_id"), nullable=False)
    business_macroprocess_id = Column(Integer, ForeignKey("business_macroprocess.business_macroprocess_id"), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationProcess(DbModel):
    __tablename__ = "organization_business_process"

    organization_business_process_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.organization_id"), nullable=False)
    business_macroprocess_id = Column(Integer, ForeignKey("business_macroprocess.business_macroprocess_id"), nullable=False)
    business_process_id = Column(Integer, ForeignKey("business_process.business_process_id"), nullable=False)
    relevance_level_id = Column(Integer, ForeignKey("basic_classification_level.basic_classification_level_id"))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationITService(DbModel):
    __tablename__ = "organization_it_service"

    organization_information_service_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.organization_id"), nullable=False)
    business_process_id = Column(Integer, ForeignKey("business_process.business_process_id"), nullable=False)
    it_service_id = Column(Integer, ForeignKey("it_service.it_service_id"), nullable=False)
    relevance_level_id = Column(Integer, ForeignKey("basic_classification_level.basic_classification_level_id"))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationITAsset(DbModel):
    __tablename__ = "organization_it_asset"

    organization_information_asset_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.organization_id"), nullable=False)
    it_service_id = Column(Integer, ForeignKey("it_service.it_service_id"), nullable=False)
    it_asset_id = Column(Integer, ForeignKey("it_asset.it_asset_id"), nullable=False)
    relevance_level_id = Column(Integer, ForeignKey("basic_classification_level.basic_classification_level_id"))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationSecurityThreat(DbModel):
    __tablename__ = "organization_security_threat"

    organization_information_asset_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.organization_id"), nullable=False)
    security_threat_id = Column(Integer, ForeignKey("security_threat.security_threat_id"), nullable=False)
    exposure_level_id = Column(Integer, ForeignKey("basic_classification_level.basic_classification_level_id"), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationITAssetVulnerability(DbModel):
    __tablename__ = "organization_it_asset_vulnerability"

    organization_information_asset_vulnerability_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.organization_id"), nullable=False)
    security_threat_id = Column(Integer, ForeignKey("security_threat.security_threat_id"), nullable=False)
    it_asset_id = Column(Integer, ForeignKey("it_asset.it_asset_id"), nullable=False)
    vulnerability_level_id = Column(Integer, ForeignKey("basic_classification_level.basic_classification_level_id"), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationVulnerabilityControl(DbModel):
    __tablename__ = "organization_vulnerability_control"

    organization_vulnerability_control_id = Column(Integer, primary_key=True)
    organization_it_asset_vulnerability_id = Column(Integer, ForeignKey("organization_it_asset_vulnerability.organization_it_asset_vulnerability_id"), nullable=False)
    controller_it_asset_id = Column(Integer, ForeignKey("organization_it_asset.organization_it_asset_id"))
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)
