from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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

    id = Column("organization_id", Integer, primary_key=True)
    tax_id = Column(String, nullable=False)
    legal_name = Column(String, nullable=False)
    trade_name = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationLocation(DbModel):
    __tablename__ = "organization_location"

    id = Column("organization_location_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id))
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

    id = Column("business_department_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class BusinessMacroprocess(DbModel):
    __tablename__ = "business_macroprocess"

    id = Column("business_macroprocess_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class BusinessProcess(DbModel):
    __tablename__ = "business_process"

    id = Column("business_process_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class ITService(DbModel):
    __tablename__ = "it_service"

    id = Column("it_service_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class ITAssetCategory(DbModel):
    __tablename__ = "it_asset_category"

    id = Column("it_asset_category_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class ITAsset(DbModel):
    __tablename__ = "it_asset"

    id = Column("it_asset_id", Integer, primary_key=True)
    category_id = Column("it_asset_category_id", Integer, ForeignKey(ITAssetCategory.id), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class SecurityThreat(DbModel):
    __tablename__ = "security_threat"

    id = Column("security_threat_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class VulnerabilityControl(DbModel):
    __tablename__ = "vulnerability_control"

    id = Column("vulnerability_control_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class SystemUser(DbModel):
    __tablename__ = "system_user"

    id = Column("system_user_id", Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    last_logged_in_on = Column(DateTime)
    last_login_attempted_on = Column(DateTime)
    failed_login_attempt_count = Column(Integer, nullable=False, default=0)
    locked_out_on = Column(DateTime)
    blocked_on = Column(DateTime)


class SystemAdministrativeRole(DbModel):
    __tablename__ = "system_administrative_role"

    id = Column("system_administrative_role_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class SystemUserAdministrativeRole(DbModel):
    __tablename__ = "system_user_administrative_role"

    id = Column("system_user_administrative_role_id", Integer, primary_key=True)
    system_user_id = Column(Integer, ForeignKey(SystemUser.id), nullable=False)
    system_administrative_role_id = Column(Integer, ForeignKey(SystemAdministrativeRole.id), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class RatingLevel(DbModel):
    __tablename__ = "rating_level"

    id = Column("rating_level_id", Integer, primary_key=True)
    name = Column(String, nullable=False)


class OrganizationDepartment(DbModel):
    __tablename__ = "organization_department"

    id = Column("organization_department_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    department_id = Column("business_department_id", Integer, ForeignKey(BusinessDepartment.id), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    department = relationship(BusinessDepartment)


class OrganizationMacroprocess(DbModel):
    __tablename__ = "organization_macroprocess"

    instance_id = Column("organization_macroprocess_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    department_id = Column("business_department_id", Integer, ForeignKey(BusinessDepartment.id), nullable=False)
    macroprocess_id = Column("business_macroprocess_id", Integer, ForeignKey(BusinessMacroprocess.id), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    department = relationship(BusinessDepartment, lazy='joined')
    macroprocess = relationship(BusinessMacroprocess, lazy='joined')


class OrganizationProcess(DbModel):
    __tablename__ = "organization_process"

    instance_id = Column("organization_process_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    macroprocess_instance_id = Column("organization_macroprocess_id", Integer, ForeignKey(OrganizationMacroprocess.instance_id), nullable=False)
    process_id = Column("business_process_id", Integer, ForeignKey(BusinessProcess.id), nullable=False)
    relevance_level_id = Column(Integer, ForeignKey(RatingLevel.id))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    process = relationship(BusinessProcess, lazy='joined')


class OrganizationITService(DbModel):
    __tablename__ = "organization_it_service"

    instance_id = Column("organization_it_service_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    process_instance_id = Column("organization_process_id", Integer, ForeignKey(OrganizationProcess.instance_id), nullable=False)
    it_service_id = Column(Integer, ForeignKey(ITService.id), nullable=False)
    relevance_level_id = Column(Integer, ForeignKey(RatingLevel.id))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    it_service = relationship(ITService, lazy='joined')


class OrganizationITAsset(DbModel):
    __tablename__ = "organization_it_asset"

    instance_id = Column("organization_it_asset_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    it_service_instance_id = Column("organization_it_service_id", Integer, ForeignKey(OrganizationITService.instance_id), nullable=False)
    it_asset_id = Column(Integer, ForeignKey(ITAsset.id), nullable=False)
    relevance_level_id = Column(Integer, ForeignKey(RatingLevel.id))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    it_asset = relationship(ITAsset, lazy='joined')


class OrganizationSecurityThreat(DbModel):
    __tablename__ = "organization_security_threat"

    id = Column("organization_security_threat_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    security_threat_id = Column(Integer, ForeignKey(SecurityThreat.id), nullable=False)
    exposure_level_id = Column(Integer, ForeignKey(RatingLevel.id), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    security_threat = relationship(SecurityThreat, lazy='joined')


class OrganizationITAssetVulnerability(DbModel):
    __tablename__ = "organization_it_asset_vulnerability"

    id = Column("organization_it_asset_vulnerability_id", Integer, primary_key=True)
    organization_security_threat_id = Column(Integer, ForeignKey(OrganizationSecurityThreat.id), nullable=False)
    it_asset_instance_id = Column("organization_it_asset_id", Integer, ForeignKey(OrganizationITAsset.instance_id), nullable=False)
    vulnerability_level_id = Column(Integer, ForeignKey(RatingLevel.id), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    organization_security_threat = relationship(OrganizationSecurityThreat, lazy='joined')
    security_threat = association_proxy('organization_security_threat', 'security_threat')

    it_asset_instance = relationship(OrganizationITAsset, lazy='joined')
    it_asset = association_proxy('it_asset_instance', 'it_asset')


class OrganizationVulnerabilityControl(DbModel):
    __tablename__ = "organization_vulnerability_control"

    id = Column("organization_vulnerability_control_id", Integer, primary_key=True)
    controlled_it_asset_id = Column(Integer, ForeignKey(OrganizationITAsset.instance_id))
    mitigating_it_asset_id = Column(Integer, ForeignKey(OrganizationITAsset.instance_id))
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)
