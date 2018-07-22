from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from knoweak.settings import DATABASE

conn_string = "mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}".format(**DATABASE)
engine = create_engine(conn_string, echo=True)
Session = sessionmaker(bind=engine)
