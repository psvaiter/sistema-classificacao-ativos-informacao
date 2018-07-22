from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from knoweak.db.models import DbModel
from knoweak.db.models.user import SystemUser


class RatingLevel(DbModel):
    __tablename__ = "rating_level"

    id = Column("rating_level_id", Integer, primary_key=True)
    name = Column(String, nullable=False)


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
