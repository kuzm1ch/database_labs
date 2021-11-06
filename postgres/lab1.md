## Лабораторна робота №1
### Знайомство із PostgreSQL
<img src='../img/logo.png' width=200/>

#### Мета: знайомство із СУБД PostgreSQL, її області використання, способи інсталювання та керування.
Лабораторна робота побудована із використанням відкритого ресурсу www.postgresqltutorial.com .

#### Що таке PostgreSQL
* PostgreSQL — це реляційна СУБД з відкритою кодовою базою. PostgreSQL підтримує як SQL (реляційні), так і JSON (нереляційні) запити.
* PostgreSQL — це високостабільна база даних, що підтримується та активно розроблюється open-source спільнотою більш ніж 20 років.
* PostgreSQL використовується як основна база даних для багатьох веб, мобільних і аналітичних додатків.
* PostgreSQL-спільнота вимовляє PostgreSQL як /ˈpoʊstɡrɛs ˌkjuː ˈɛl/.

#### Історія PostgreSQL
Проект PostgreSQL розпочався в 1986 році на факультеті комп’ютерних наук Берклі Каліфорнійського університету. Початкова назва була POSTGRES, посилаючись на стару базу даних Ingres, яку також була розроблено в Берклі. Метою POSTGRES було додати функції, що необхідні для підтримки різних типів даних. У 1996 році проект POSTGRES був перейменований на PostgreSQL, щоб чітко проілюструвати його підтримку SQL. Сьогодні PostgreSQL зазвичай скорочується як Postgres. Із 1996 Група глобальної розробки PostgreSQL(PostgreSQL Global Development Group), спеціальна спільнота учасників, продовжує випускати безплатні версії бази даних із відкритим кодом. Спочатку PostgreSQL був розроблений для роботи тільки на UNIX-подібних платформах, пізніше були доопрацювання, що дозволили її запускати на Windows, macOS і Solaris.

#### Області використання СУБД PostgreSQL
Області використання PostgreSQL дуже широкі, нижче наведені деякі приклади.
1. Надійна база даних у стеку LAPP.  
LAPP означає Linux, Apache, PostgreSQL і PHP (або Python і Perl). PostgreSQL виконує ф-ції надійного внутрішнього сховища даних, яку використовують багато динамічних веб-сайтів і веб-додатків.
2. Транзакційна база даних загального призначення.  
Великі корпорації та стартапи використовують PostgreSQL як основну базу даних для підтримки своїх програм і продуктів.
3.  Геопросторова база даних.  
PostgreSQL з розширенням PostGIS підтримує геопросторові дані для геоінформаційних систем (GIS).

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

##### Вимоги до оформлення
Звіт лабораторної роботи повинен містити текстову частину завдання і скріншоти із командами та відповідним виводом. В кінці звіту обов'язково повинен бути висновок.