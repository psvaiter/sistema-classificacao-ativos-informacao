# System Configuration

**DEVELOPMENT CONFIGURATION**
```
OS: Windows 10 (64-bit)
IDE: Visual Studio Code
Python 3.6.3 (both 32-bit and 64-bit installed)
    pip is available
    pipenv installed for user with command "pip install --user pipenv". Added to PATH environment variable manually.
Database: MySQL Community Edition (GPL)
    MySQL Installer 5.7.19 (Windows)
    Setup type: Developer default
    Python connector failed. Missing Python 64-bit...
    Standalone MySQL Server
        Development machine
        TCP/IP Port 3306
        Root's password: root
        psvaiter's password (DB Admin): admin
        Configured as a Windows Service (Run as Standard System Account)
        Enable X Protocol / MySQL as a Document Store (Port: 33060)
        Server Id: 1
    Notes:
        Default database engine: InnoDB 5.7.19
```     

**PRODUCTION CONFIGURATION**

```
OS: FreeBSD v11.1
Database: MySQL Community Edition (GPL)
Python 3.6.3
    
    Check if pip is available
      $ pip --version
      If not, install pip separately. Instructions at https://pip.pypa.io/en/stable/installing/
    
    Install pipenv:
      pip install --user pipenv
      
      "If pipenv isn't available in your shell after installation, you'll 
      need to add the user base's binary directory to your PATH.
      
      On Linux and macOS you can find the user base binary directory by running 
      python -m site --user-base and adding bin to the end. 
      For example, this will typically print ~/.local (with ~ expanded to the 
      absolute path to your home directory) so you’ll need to add ~/.local/bin to 
      your PATH. You can set your PATH permanently by modifying ~/.profile."
    
    http://docs.python-guide.org/en/latest/dev/virtualenvs/
    
Web server: Apache 2.x
```

## Architecture

1 front-end web application that consumes resources from a back-end web API.  
1 back-end web API that interacts with database and performs input validations.  
1 MySQL database.

## Project decisions

### Database Management System

**MySQL** was chosen because it meets all of the following project requirements:

- SQL database
- Compatible with FreeBSD
- ACID compliant (when using InnoDB engine)
- Open source
- Licenses allowed: GPL, Apache?, BSD?...
    
**Why not PostgreSQL?**

PostgreSQL also meets the requirements, but:

- MySQL meets all the minimum requirements to make the project viable.
- PostgreSQL does not add any essential functionality that increases the project quality or productivity.
- PostgreSQL would be more appropriate for higher loads and more concurrent accesses than will actually happen.

A deeper comparison can be seen at https://www.2ndquadrant.com/en/postgresql/postgresql-vs-mysql/.

### Programming language

**Why Python?**

- Compatible with FreeBSD, cross-platform.
- Fast prototyping.
    
**Why not C, C++, C# .NET or Java?**

- No Java knowledge. Java is supported by FreeBSD.
- Great knowledge in .NET platform. .NET Core is open source and cross-platform, but hasn't been ported to FreeBSD yet. All major Linux distros are supported.
- C is very low level to achieve our goals. There's no need to make it that way if we can be more productive with other languages.
- C++ would be a good choice, but as a compiled language, deployment process would be more complicated due to the need to build all other dependencies in the target platform. This process usually causes some headache.

### Back-end
        
    Python API frameworks
        Falcon (https://falconframework.org/)
        Flask (Flask RESTful vs Flask API)
        Bottle (http://bottlepy.org/docs/dev/index.html)
        Pecan
        Werkzeug
        Django
        API star (https://github.com/encode/apistar)
        ButterflyNet
        Uvloop
        Morepath
        Eve
        Sanic
        Hug (https://github.com/timothycrosley/hug) uses Falcon
        https://www.fullstackpython.com/api-creation.html
        https://www.quora.com/What-is-a-good-Python-framework-for-building-a-RESTful-API
        http://wsgi.readthedocs.io/en/latest/what.html
        https://www.infoworld.com/article/3133854/application-development/5-wicked-fast-python-frameworks-you-have-to-try.html
        https://wiki.python.org/moin/WebFrameworks
        http://steelkiwi.com/blog/best-python-web-frameworks-to-learn/
    
    Routes:
        
    ORM?

## MySQL database

Database name: InformationAssets

EER diagram:
[](link to image)
    
    
PyPy vs CPython

API Documentation  
Logging  
Web application authentication (no authorization)  
Unicode support is not a requirement  
