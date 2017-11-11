# Database Modeling

Database name: `db_information_asset_security`

## Relationships in fluid sentences

Below there's a list of sentences describing the relationships between the entities of the system.  
Our intention is to extract entities from specification.

- Each **organization** have one or more **departments**.
- Each **department** have one or more **macroprocesses**.
- Each **macroprocess** is divided into one or more **processes**.
- Each **process** is supported by one or more **information services**.
- Each **information service** is supported by one or more **information assets**.
- Each **information asset** belongs to one **category**.
- Each **information asset** have zero or more **vulnerabilities**.
- Each **security threat** targets one or more **vulnerabilities** of different information assets.
- Each **organization** implements one or more **controls** to mitigate vulnerabilities of information assets.
- Each **organization** have zero or one head office **address**.
- Each **system user** have one or more **system adminsitrative roles**.
- Each **system user** creates one or more **risk analysis reports** of information security incidents.
- Each **risk analysis report** belongs to only one **organization**.
- Each **risk analysis report** have consolidated information about many of the other entities, thus no relationships are established with them.

From the sentences above, we extract the following entities:

- Organization
- Organization location
- Business department
- Business macroprocess
- Business process
- Information service
- Information asset
- Information asset vulnerability
- Information asset category
- Security threat
- System user
- System permission
- Risk analysis report

A department can be reused for different organizations, a macroproecess can be reused for different deparments, and so on. So all these entities must be independent, allowing a M:N relationship cardinality between them, except for Organization location (depends on Organization) and Information asset vulnerability (depends on Information asset).

## Entities' fields

Items prefixed with * are mandatory in database.

All entities have a unique identifier used to create relationships.

All entities have the record metadata `created_on` and `last_modified_on` representing the record creation timestamp and last modification timestamp respectively.

#### Organization

- *Tax ID
- *Legal name
- Trade name _(aka DBA - Doing Business As)_

#### Organization location

- *Organization identifier
- Latitude, Longitude
- Postal Code
- Country subdivision code as defined in [ISO 3166-2](https://en.wikipedia.org/wiki/ISO_3166-2)
- City name
- Street address 1
- Street address 2

All fields are optional because either (lat, long) or the other fields must be informed. If (lat, long) is informed the other fields can be searched and vice-versa.

#### Business department, Business macroprocess and Business process and Information service

- *Name _(must be unique)_

#### Information asset

- *Information asset category identifier
- *Name _(must be unique)_
- Description

#### Information asset vulnerability

- *Information asset identifier
- *Name _(must be unique)_
- Description

#### Information asset category

- *ID
- *Name _(must be unique)_

#### Security threat

- *Name _(must be unique)_
- Description

#### System user

- *Email _(must be unique)_
- *Name

#### System administrative role

- *ID
- *Name _(must be unique)_
- Description

#### System user - System administrative role (M:N)

- System user identifier
- System administrative role identifier

#### Risk analysis report

- *Name
- *Organization identifier




Faltam as tabelas associativas



## Domain data

Information asset categories:

- Hardware
- Software
- Person
- Place / Infrastructure
- Process / Policy
- Information (not clear what this means)

System administrative roles:

- Admin - full access
- MaintenanceAdmin - grants rights to manage domain data only
- UserAdmin - grants rights to manage users only
- User - grants rights to manage organizations, departments, analysis report etc.

## Naming conventions

The naming conventions used for database objects' names follows those used by MySQL database users.

MySQL is case-sensitive, so it's commonly preferred to write object names in snake_case.  
All tables are named in the singular form.  
Associative tables' names are usually the combination of the parent table names.

Indexes, foreign keys, uniques etc. are written in a convention different than that MySQL creates automatically.

- Primary keys are named `PRIMARY`.
- Foreign keys are prefixed with `fkey_` followed by the table name being referenced.
- Indexes are prefixed with `ix_`.
- Unique indexes are prefixed with `ux_` followed by the names of the columns that are unique together, each one separated by an underscore.

## EER diagram

![database-diagram-full](https://user-images.githubusercontent.com/16355712/32494677-ad22f250-c3a9-11e7-80ef-c359cd6f8113.png)