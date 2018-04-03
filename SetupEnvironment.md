## Setup development environment

#### Recommended IDEs and tools

- [MySQL Workbench 6.3+](https://dev.mysql.com/downloads/workbench/) for database modeling and querying.
- [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download) for back end development.
- [Visual Studio Code](https://code.visualstudio.com/Download) for front end development.
- [Postman](https://www.getpostman.com/apps) to discover and test the API.

#### Project requirements

- [Git](https://git-scm.com/downloads)
- [Python 3.6+](https://www.python.org/downloads/)
- [Docker CE (Community Edition)](https://www.docker.com/community-edition)
- [Node.js](https://nodejs.org/en/download/) (choose the LTS version)

### Install the project

#### Check requirements

Check that all the requirements are installed. Execute the commands below in the command 
prompt of your system.
```
> git --version
> python --version
> docker --version
> node --version
> npm --version
```
Note: The executables must be in your `PATH` environment variable in order to work.
  
#### Setup database server 

Install the Docker image of MySQL Server and run it.
```
> docker pull mysql/mysql-server:5.7
> docker run -d \
    --name mysql1 \
    --mount source=mysql1-vol,target=/var/lib/mysql \
    -p 3306:3306 \
    mysql/mysql-server:5.7
```

Next, it's required to get the generated password for 'root' and change it the first 
time you access the server. You may need to wait a few seconds for the container to start.

Also, let's create your personal user in case you need to use MySQL Workbench and a
user for the application to connect to the database.
```
> docker logs mysql1
> docker exec -it mysql1 mysql -uroot -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'insert-password-for-root-here';
mysql>
mysql> CREATE USER 'my-user'@'%' IDENTIFIED BY 'my-password';
mysql> GRANT ALL ON *.* TO 'my-user'@'%' GRANT OPTION;
mysql> SELECT host, user FROM mysql.user;
mysql>
mysql> CREATE USER 'KnoweakAppUser'@'%' IDENTIFIED BY 'app_pass';
mysql> GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'KnoweakAppUser'@'%';
mysql> exit
```

#### Deploy database

Open MySQL Workbench and connect to the database with your personal user (created in 
previous step).

Run the latest baseline script present in folder `db` of the repository.

#### Install the API

Fisrt, install the `pipenv` package manager for Python. Then install the project.
```
> pip install pipenv
> cd ~ && mkdir -p projects && cd projects
> git clone https://github.com/psvaiter/knoweak-api.git
> cd knoweak-api/src
> pipenv install --dev
```

Start the API to listen HTTP requests on port 8000.
```
> # In Windows
> waitress-serve --port 8000 app:api

> # In UNIX
> gunicorn --bind=:8000 app:api
```

Make a request with cURL to test the API.
```
> curl -s http://localhost:8000/departments | json_pp
```

#### Install the web application

Install and start the application on default port (4200).
```
> cd ~ && mkdir -p projects && cd projects
> git clone https://github.com/psvaiter/knoweak-web.git
> cd knoweak-web
> npm install
> ng serve
```

Go to the browser and visit <http://localhost:4200>.

#### You're done.

Now you have a working API communicating with a real database and a web UI set up.