FROM mysql/mysql-server:5.7

# Directory in which MySQL will look for initialization scripts
ENV MYSQL_INIT_DB_DIR=/docker-entrypoint-initdb.d
ENV INIT_DB_FILE_PATH=$MYSQL_INIT_DB_DIR/"01.sql"

COPY my.cnf /etc/my.cnf
COPY ./scripts /scripts

RUN echo "Building initialization script (01.sql)" \
    && cat /scripts/create-database.sql > $INIT_DB_FILE_PATH \
    && cat /scripts/insert-seed-data.sql >> $INIT_DB_FILE_PATH \
    && cat /scripts/create-app-user.sql >> $INIT_DB_FILE_PATH