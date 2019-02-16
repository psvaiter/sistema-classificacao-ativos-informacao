from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from knoweak.db.models import DbModel


class RatingLevel(DbModel):
    __tablename__ = "rating_level"

    id = Column("rating_level_id", Integer, primary_key=True)
    name = Column(String, nullable=False)


class SystemPermission(DbModel):
    __tablename__ = "system_permission"

    id = Column("system_permission_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class SystemRole(DbModel):
    __tablename__ = "system_role"

    id = Column("system_role_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)


class SystemRolePermission(DbModel):
    __tablename__ = "system_role_permission"

    role_id = Column("system_role_id", Integer, ForeignKey(SystemRole.id), primary_key=True)
    permission_id = Column("system_permission_id", Integer, ForeignKey(SystemPermission.id), primary_key=True)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    permission = relationship(SystemPermission, lazy='joined')
