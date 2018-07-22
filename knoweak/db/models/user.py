from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from knoweak.db.models import DbModel


class SystemUser(DbModel):
    __tablename__ = "system_user"

    id = Column("system_user_id", Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    locked_out_on = Column(DateTime)
    blocked_on = Column(DateTime)

    user_roles = relationship("SystemUserAdministrativeRole", lazy='joined')
    roles = association_proxy("user_roles", "role")


class SystemUserLogin(DbModel):
    __tablename__ = "system_user_login"

    id = Column("system_user_login_id", Integer, primary_key=True)
    system_user_id = Column(Integer, ForeignKey(SystemUser.id), nullable=False)
    attempted_on = Column(DateTime, nullable=False)
    was_successful = Column(Boolean, nullable=False)
