
MySQL = {
    'driver': "mysql+pymysql",
    'user': "psvaiter",
    'pass': "admin",
    'host': "localhost",
    'port': "3306",
    'db_name': "db_information_asset_security"
}

conn_string = "{driver}://{user}:{pass}@{host}:{port}/{db_name}".format(**MySQL)
