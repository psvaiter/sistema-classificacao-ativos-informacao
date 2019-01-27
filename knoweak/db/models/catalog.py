from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from knoweak.db.models import DbModel


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
    category_id = Column("it_asset_category_id", Integer,  ForeignKey(ITAssetCategory.id), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    category = relationship(ITAssetCategory, lazy='joined', innerjoin=True)


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
