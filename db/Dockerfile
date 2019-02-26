FROM mysql/mysql-server:5.7

# This image prepares the database to be used by knoweak-api.
# On first use (no data in volume), initialization scripts will be executed.
# MySQL will look for initialization scripts in '/docker-entrypoint-initdb.d'.
# MySQL startup options are being set in Global options file '/etc/my.cnf'.

ENV MYSQL_INIT_DB_DIR=/docker-entrypoint-initdb.d
ENV INIT_DB_FILE_PATH=$MYSQL_INIT_DB_DIR/"01.sql"

COPY my.cnf /etc/my.cnf
COPY ./scripts /scripts

RUN cat /scripts/create-database.sql > $INIT_DB_FILE_PATH \
    && cat /scripts/insert-seed-data.sql >> $INIT_DB_FILE_PATH \
    && cat /scripts/create-app-user.sql >> $INIT_DB_FILE_PATH