## Лабораторна робота №1
### PostgreSQL. Встановлення з'єднання використовуючи Python.
<img src='img/logo.png' width=350/>

#### Мета: знайомство із принципом встановлення з'єднання до бази даних із використанням мови програмування Python
Лабораторна робота побудована із використанням відкритого ресурсу www.postgresqltutorial.com .

#### Мова програмування Python(короткі відомості)
* Python  – динамічна інтерпретована об’єктно-орієнтована скриптова мова програмування із строгою динамічною типізацією. Розроблена в 1990 році голландським програмістом Гвідо ван Россумом .
* Автор назвав мову на честь популярного британського комедійного серіалу 1970-х років "Летючий цирк Монті Пайтона». Найчастіше вживане прочитання назви мови — «Па́йтон».
* Офіційний сайт мови програмування Python https://www.python.org/ .
* Python – багатоцільова мова програмування, яка дозволяє писати код, що добре читається. Відносний лаконізм мови Python дозволяє створити програму, яка буде набагато коротше свого аналога, написаного на іншій мові.
* Python - багатоплатформова мова програмування. Це означає, що програми на Python можна запускати в різних операційних системах без будь-яких змін.
* Ще однією перевагою Python є його стандартна бібліотека, яка встановлюється разом з Python і містить готові інструменти для роботи з операційною системою, веб-сторінками, базами даних, різними форматами даних, для побудови графічного інтерфейсу програм тощо.
* Програми, написані на мові програмування Python, можуть бути як невеликими скриптами, так і складними системами.
* Python безкоштовний у використанні та із відкритим кодом(Open source) https://github.com/python .


#### psycopg адаптер
* В даній роботі з'єднання буде встановлено із використанням psycopg python адаптеру. Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Its main features are the complete implementation of the Python DB API 2.0 specification and the thread safety (several threads can share the same connection). It was designed for heavily multi-threaded applications that create and destroy lots of cursors and make a large number of concurrent “INSERT”s or “UPDATE”s. 

* Psycopg 2 is mostly implemented in C as a libpq wrapper, resulting in being both efficient and secure. It features client-side and server-side cursors, asynchronous communication and notifications, “COPY TO/COPY FROM” support. Many Python types are supported out-of-the-box and adapted to matching PostgreSQL data types; adaptation can be extended and customized thanks to a flexible objects adaptation system. Psycopg 2 is both Unicode and Python 3 friendly.

* Встановлення psycopg слід виконати із допомогою пакетного менеджера мови Python - pip, який буде автоматично встановлений, якщо Python був завантажений із python.org . В протилежному випадку можна скористатись [документацією](https://pip.pypa.io/en/stable/installation/).

### 🎯 Завдання
На сайті https://www.postgresqltutorial.com/ пройти курс [PostgreSQL Python: Connect To PostgreSQL Database Server](https://www.postgresqltutorial.com/postgresql-python/connect/) та  оформити прогрес у вигляді звіту.
[PostgreSQL Python: Connect To PostgreSQL Database Server](https://www.postgresqltutorial.com/postgresql-python/connect/) містить такі основні пункти: 
- встановлення psycopg2 адaптеру для спілкування із БД;
- під'єднатись до БД із використанням python скрипта `connect.py`.  Параметри з'єднання винесені у файл `database.ini`.

Окрім завдань описаних в курсі слід виконати і наступне: 
1. створити базу даних із назвою "NameSurname", що відповідє вашому імені та прізвищу, наприклад "IvanIvanov", і саме до неї встановлювати з'єднання (параметр `database` в `database.ini`);
2. окрім версії СУБД ваш скрипт повинен виводити назву поточної бази даних(наприклад `IvanIvanov`).

##### Вимоги до оформлення
Звіт лабораторної роботи повинен містити текстову частину завдання і скріншоти із командами та відповідним виводом. В кінці звіту обов'язково повинен бути висновок.
