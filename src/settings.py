
MySQL = {
    'driver': "mysql+pymysql",
    'user': "ITSecurityControlAppUser",
    'pass': "app_pass",
    'host': "localhost",
    'port': "3306",
    'db_name': "db_information_asset_security"
}

conn_string = "{driver}://{user}:{pass}@{host}:{port}/{db_name}".format(**MySQL)
