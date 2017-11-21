# Database Modeling

Database name: `db_information_asset_security`

## Relationships in fluid sentences

Below there's a list of sentences describing the relationships between the entities of the system.  
Our intention is to extract entities from specification.

- Each **organization** has zero or more **departments**.
- Each **department** belongs to zero or more **organizations**.
- Each **department** has zero or more **macroprocesses**.
- Each **macroprocess** is used by zero or more **departments**.
- Each **macroprocess** comprehends zero or more **processes**.
- Each **process** is used by zero or more **macroprocesses**.
- Each **process** is supported by zero or more **information services**.
- Each **information service** supports zero or more **processes**.
- Each **information service** is supported by zero or more **information assets**.
- Each **information asset** supports zero or more **information services**.
- Each **information asset** belongs to one **category**.
- Each **organization** is exposed to zero or more **security threats**.
- Each **security threat** exposes zero or more **organizations** to security incidents.
- Each **security threat** explores vulnerabilities of zero or more **information assets** of an **organization**.
- Each **information asset** of an **organization** has a degree of vulnerability to a **security threat** to which the **organization** is exposed **(= organization information asset vulnerability)**. An information asset belongs to an organization if it supports at least one information service that supports a process inside the macroprocess of an organization department, thus this relationship is not explicit in database.
- Each **organization infromation asset vulnerability** to a security threat can be mitigated by implementing one or more **controls**.
- Each **organization vulnerability control** targets a specific **organization information asset vulnerability** to a security threat.
- Each **organization vulnerability control** for an **information asset** can be implemented with another **information asset** or not **`<-- CONFIRM: can or must?`**.
- Each **organization** has zero or one head office **address**.
- Each **system user** has zero or more **system adminsitrative roles**.
- Each **system user** creates one or more **risk analysis reports** of information security incidents.
- Each **risk analysis report** belongs to only one **organization**.
- Each **risk analysis report** has consolidated information about many of the other entities, thus no relationships are established with them.

From the sentences above, we extract the following entities:

- Organization
- Organization location
- Business department
- Business macroprocess
- Business process
- Information service
- Information asset
- Information asset category
- Security threat
- Organization security threat
- Organization information asset vulnerability
- Organization vulnerability control
- System user
- System administrative role
- Risk analysis report

A department can be reused for different organizations, a macroproecess can be reused for different deparments, and so on. So all these entities must be independent, allowing a M:N relationship cardinality between them, except for Organization location (depends on Organization) and Information asset vulnerability (depends on Information asset).

## Data Dictionary

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
- Country code as defined in [ISO 3166-1 alpha 2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
- Postal Code
- Country subdivision code as defined in [ISO 3166-2](https://en.wikipedia.org/wiki/ISO_3166-2) (second part)
- City name
- Street address 1
- Street address 2

All fields are optional because either (lat, long) or the other fields must be informed. If (lat, long) is informed the other fields can be searched and vice-versa.

#### Business department, Business macroprocess, Business process and Information service

- *Name _(must be unique)_

#### Information asset

- *Identifier of the information asset category
- *Name
- Description

Name must be unique for a given category.

#### Information asset category

- *ID
- *Name _(must be unique)_

#### Security threat

- *Name _(must be unique)_
- Description

#### Organization security threat

Each organization is exposed to a security threat at a specific degree.

- *Organization identifier
- *Security threat identifier
- *Exposure level (see Basic classification level)

#### Organization information asset vulnerability

Each information asset may have a different vulnerability level to a security threat inside an organization.

- *Organization identifier
- *Identifier of the information asset
- *Identifier of the security threat
- *Vulnerability level (see Basic classification level)

#### Organization vulnerability control

- *Identifier of organization information asset vulnerability
- Identifier of information asset that mitigates the vulnerability
- Description

Either (information asset that acts as a controller) or (description) is mandatory.

#### System user

- *Email _(must be unique)_
- *Name
- Password
- Last login date and time

Password is optional because system user may use other authentication method to login.

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
- UserAdmin - grants rights to manage users only
- User - grants rights to manage organizations, departments, analysis report etc.

## Naming conventions

The naming conventions used for database objects follows those used by MySQL database users.

- `snake_case`
- Tables are named in the singular form.
- Names of associative tables are usually the combination of the parent table names.

Foreign keys, indexes, and unique constraints are written in a convention different than that MySQL suggests when creating them.

| Object       | Name convention                          |
| ------------ | ---------------------------------------- |
| Primary key  | `PRIMARY`                                |
| Foreign key  | `FK_TableName_OtherTableName`            |
| Index        | `IX_TableName_IndexedColumn1_IndexedColumn2` |
| Unique index | `UQ_TableName_IndexedColumn1_IndexedColumn2` |

*You may find table names abbreviated on some indexes and foreign keys. That's because the max length allowed for object names in MySQL is 64 characters and the concatenation of table names overflows this limit.*

## EER diagram

![database-diagram-full](https://user-images.githubusercontent.com/16355712/32494677-ad22f250-c3a9-11e7-80ef-c359cd6f8113.png)