import os


DATABASE = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', 3306),
    'username': os.environ.get('DB_USERNAME', 'KnoweakAppUser'),
    'password': os.environ.get('DB_PASSWORD'),
    'db_name': os.environ.get('DB_NAME', 'knoweak')
}

conn_string = "mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}".format(**DATABASE)
