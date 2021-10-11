## Лабораторна робота №1
### Знайомство із PostgreSQL
<img src='../img/logo.png' width=200/>

#### Мета: знайомство із СУБД PostgreSQL, її області використання, способи інсталювання та керування.
Лабораторна робота побудована із використанням відкритого ресурсу www.postgresqltutorial.com .

#### Що таке PostgreSQL
* PostgreSQL is an advanced, enterprise-class, and open-source relational database system. PostgreSQL supports both SQL (relational) and JSON (non-relational) querying.
* PostgreSQL is a highly stable database backed by more than 20 years of development by the open-source community.
* PostgreSQL is used as a primary database for many web applications as well as mobile and analytics applications.
* PostgreSQL’s community pronounces PostgreSQL as /ˈpoʊstɡrɛs ˌkjuː ˈɛl/.

#### Історія PostgreSQL
The PostgreSQL project started in 1986 at Berkeley Computer Science Department, University of California. The project was originally named POSTGRES, in reference to the older Ingres database which also developed at Berkeley. The goal of the POSTGRES project was to add the minimal features needed to support multiple data types. In 1996, the POSTGRES project was renamed to PostgreSQL to clearly illustrate its support for SQL. Today, PostgreSQL is commonly abbreviated as Postgres. Since then, the PostgreSQL Global Development Group, a dedicated community of contributors continues to make the releases of the open-source and free database project. Originally, PostgreSQL was designed to run on UNIX-like platforms. And then, PostgreSQL was evolved run on various platforms such as Windows, macOS, and Solaris.

#### Області використання СУБД PostgreSQL
The following are the common use cases of PostgreSQL.
1. A robust database in the LAPP stack
LAPP stands for Linux, Apache, PostgreSQL, and PHP (or Python and Perl). PostgreSQL is primarily used as a robust back-end database that powers many dynamic websites and web applications.
2. General purpose transaction database
Large corporations and startups alike use PostgreSQL as primary databases to support their applications and products.
3.  Geospatial database
PostgreSQL with the PostGIS extension supports geospatial databases for geographic information systems (GIS).

### 🎯 Завдання
На сайті https://www.postgresqltutorial.com/ пройти курс [getting started](https://www.postgresqltutorial.com/postgresql-getting-started) та  оформити прогрес у вигляді звіту.
[Getting started курс](https://www.postgresqltutorial.com/postgresql-getting-started) включає в себе такі основні пункти: 
- Інсталювання
- Встановлення з'єднання з допомогою інтерфейса командого рядку(CLI) psql та веб-застосунку pgAdmin.
- Завантаження тестової бази даних DVD Rental(psql/pgAdmin).

Зверніть уваги, що інсталювати потрібно для однієї опреаційної системи на ваш вибір(Unix/Windows/MacOS), не потрібно це роботи одночасно для всіх. З'єднання повинно бути встановлена із допомогою psql та pgAdmin. Завантаження тестової бази потрібно роити в такому порядку:
1. завантажити дамп бази DVD Rental з допомогою psql
2. командою SQL(`SELECT * from dvdrental`) показати, що база було завантажено
3. видалити DVD Rental(`DROP dvdrental`)
4. завантажити дамп бази DVD Rental з допомогою pgAdmin
5. показати на скріні(pgAdmin), що базу було успішно завантажено
6. створіть в даній базі(dvdrental) нову таблицю із назвою, що дорівнює вашій фамілії, та колонками id, date, name.

Ivanov_table
| id | nane | date |
|----|------|------|
| -  |  -   |   -  |
| -  |  -   |   -  |
