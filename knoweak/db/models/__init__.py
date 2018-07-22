from dictalchemy import make_class_dictable
from sqlalchemy.ext.declarative import declarative_base

DbModel = declarative_base()
make_class_dictable(DbModel)
