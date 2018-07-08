from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dictalchemy import make_class_dictable
from datetime import datetime
from knoweak.settings import conn_string

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


class MitigationControl(DbModel):
    __tablename__ = "mitigation_control"

    id = Column("mitigation_control_id", Integer, primary_key=True)
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

    user_roles = relationship("SystemUserAdministrativeRole", lazy='joined')
    roles = association_proxy("user_roles", "role")


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
    user_id = Column("system_user_id", Integer, ForeignKey(SystemUser.id), nullable=False)
    role_id = Column("system_administrative_role_id", Integer, ForeignKey(SystemAdministrativeRole.id), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    role = relationship(SystemAdministrativeRole, lazy='joined')


class RatingLevel(DbModel):
    __tablename__ = "rating_level"

    id = Column("rating_level_id", Integer, primary_key=True)
    name = Column(String, nullable=False)


class OrganizationDepartment(DbModel):
    __tablename__ = "organization_department"

    organization_id = Column(Integer, ForeignKey(Organization.id), primary_key=True)
    department_id = Column("business_department_id", Integer, ForeignKey(BusinessDepartment.id), primary_key=True)
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

    department = relationship(BusinessDepartment, lazy='joined', innerjoin=True)
    macroprocess = relationship(BusinessMacroprocess, lazy='joined', innerjoin=True)


class OrganizationProcess(DbModel):
    __tablename__ = "organization_process"

    instance_id = Column("organization_process_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    macroprocess_instance_id = Column("organization_macroprocess_id", Integer, ForeignKey(OrganizationMacroprocess.instance_id), nullable=False)
    process_id = Column("business_process_id", Integer, ForeignKey(BusinessProcess.id), nullable=False)
    relevance_level_id = Column(Integer, ForeignKey(RatingLevel.id))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    process = relationship(BusinessProcess, lazy='joined', innerjoin=True)


class OrganizationITService(DbModel):
    __tablename__ = "organization_it_service"

    instance_id = Column("organization_it_service_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    process_instance_id = Column("organization_process_id", Integer, ForeignKey(OrganizationProcess.instance_id), nullable=False)
    it_service_id = Column(Integer, ForeignKey(ITService.id), nullable=False)
    relevance_level_id = Column(Integer, ForeignKey(RatingLevel.id))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    it_service = relationship(ITService, lazy='joined', innerjoin=True)
    # organization_it_assets = relationship("OrganizationITAsset", secondary="OrganizationITServiceITAsset")
    # it_assets = association_proxy("organization_it_assets", "it_asset")


class OrganizationITAsset(DbModel):
    __tablename__ = "organization_it_asset"

    instance_id = Column("organization_it_asset_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    it_asset_id = Column(Integer, ForeignKey(ITAsset.id), nullable=False)
    external_identifier = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    it_asset = relationship(ITAsset, lazy='joined', innerjoin=True)


class OrganizationITServiceITAsset(DbModel):
    __tablename__ = "organization_it_service_it_asset"

    it_service_instance_id = Column("organization_it_service_id", Integer, ForeignKey(OrganizationITService.instance_id), primary_key=True)
    it_asset_instance_id = Column("organization_it_asset_id", Integer, ForeignKey(OrganizationITAsset.instance_id), primary_key=True)
    relevance_level_id = Column(Integer, ForeignKey(RatingLevel.id))
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    it_service_instance = relationship(OrganizationITService, lazy='joined', innerjoin=True)
    it_service = association_proxy("it_service_instance", "it_service")
    it_asset_instance = relationship(OrganizationITAsset, lazy='joined', innerjoin=True)
    it_asset = association_proxy("it_asset_instance", "it_asset")


class OrganizationSecurityThreat(DbModel):
    __tablename__ = "organization_security_threat"

    id = Column("organization_security_threat_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    security_threat_id = Column(Integer, ForeignKey(SecurityThreat.id), nullable=False)
    threat_level_id = Column(Integer, ForeignKey(RatingLevel.id), nullable=False)
    # threatening_organization_it_asset_id = Column(Integer, ForeignKey(), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    security_threat = relationship(SecurityThreat, lazy='joined', innerjoin=True)


class OrganizationITAssetVulnerability(DbModel):
    __tablename__ = "organization_it_asset_vulnerability"

    id = Column("organization_it_asset_vulnerability_id", Integer, primary_key=True)
    organization_security_threat_id = Column(Integer, ForeignKey(OrganizationSecurityThreat.id), nullable=False)
    it_asset_instance_id = Column("organization_it_asset_id", Integer, ForeignKey(OrganizationITAsset.instance_id), nullable=False)
    vulnerability_level_id = Column(Integer, ForeignKey(RatingLevel.id), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    organization_security_threat = relationship(OrganizationSecurityThreat, lazy='joined', innerjoin=True)
    security_threat = association_proxy('organization_security_threat', 'security_threat')

    it_asset_instance = relationship(OrganizationITAsset, lazy='joined', innerjoin=True)
    it_asset = association_proxy('it_asset_instance', 'it_asset')


class OrganizationVulnerabilityControl(DbModel):
    __tablename__ = "organization_vulnerability_control"

    id = Column("organization_vulnerability_control_id", Integer, primary_key=True)
    organization_it_asset_vulnerability_id = Column(Integer, ForeignKey(OrganizationITAssetVulnerability.id), nullable=False)
    mitigation_control_id = Column(Integer, ForeignKey(MitigationControl.id), nullable=False)
    mitigating_it_asset_id = Column(Integer, ForeignKey(OrganizationITAsset.instance_id))
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    mitigation_control = relationship(MitigationControl, lazy='joined', innerjoin=True)
    mitigating_it_asset = relationship(OrganizationITAsset, lazy='joined')


class OrganizationAnalysis(DbModel):
    __tablename__ = "organization_analysis"

    id = Column("organization_analysis_id", Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey(Organization.id), nullable=False)
    description = Column(String)
    analysis_performed_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class OrganizationAnalysisDetail(DbModel):
    __tablename__ = "organization_analysis_detail"

    id = Column("organization_analysis_detail_id", Integer, primary_key=True)
    organization_analysis_id = Column(Integer, ForeignKey(OrganizationAnalysis.id), nullable=False)
    department_name = Column(String, nullable=False)
    macroprocess_name = Column(String, nullable=False)
    process_name = Column(String, nullable=False)
    process_relevance = Column(Integer, nullable=False)
    it_service_name = Column(String, nullable=False)
    it_service_relevance = Column(Integer, nullable=False)
    it_asset_name = Column(String, nullable=False)
    it_asset_relevance = Column(Integer, nullable=False)
    calculated_impact = Column(Float, nullable=False)
    security_threat_name = Column(String, nullable=False)
    security_threat_level = Column(Integer, nullable=False)
    it_asset_vulnerability_level = Column(Integer, nullable=False)
    calculated_probability = Column(Float, nullable=False)
    calculated_risk = Column(Float, nullable=False)
