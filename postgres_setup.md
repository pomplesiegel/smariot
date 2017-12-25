### Local Installation
```
$ sudo apt-get install postgresql pgadmin3
...
$ which psql
/usr/bin/psql
```
- After installation, follow [steps](http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/firstconnect.html) for the first run (set password, enable local access etc)
- For python libs/dependencies run `pip3 install Flask-SQLAlchemy psycopg2`
- For GUI use `pgadmin3`, similar to `phpMyAdmin`

### Create Database
```
$ psql -U postgres
Password for user postgres: 
psql (9.5.10)
Type "help" for help.

postgres=# CREATE DATABASE smariot;
CREATE DATABASE
postgres=# CREATE USER smariot_app WITH PASSWORD 'iot123';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE smariot TO smariot_app;
GRANT
postgres=# \q
```

### Export Env Vars
`$ export DATABASE_URL=postgres://smariot_app:iot123@localhost/smariot`

### Create Tables etc
```
$ python3
Python 3.5.2 (default, Nov 23 2017, 16:37:01) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from app import db
>>> db.create_all()
```
- Ensure there are no errors while running `db.create_all()`

### Inspecting DB Contents
```
$ psql -U postgres
...
postgres=# \connect smariot
You are now connected to database "smariot" as user "postgres".
smariot=# \l
                                   List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |    Access privileges     
-----------+----------+----------+-------------+-------------+--------------------------
...
 smariot   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/postgres            +
           |          |          |             |             | postgres=CTc/postgres   +
...
(4 rows)

smariot=# \dt
          List of relations
 Schema | Name | Type  |    Owner    
--------+------+-------+-------------
 public | data | table | smariot_app
(1 row)

smariot=# SELECT * FROM data;

... Data ...

smariot=# \q
```

### Remote (Heroku) Installation
- Follow Heroku's [docs](https://devcenter.heroku.com/articles/heroku-postgresql)
- Make changes and test in local, push code to `GitHub` (or Heroku's Git)
- Run `heroku run python3` and execute `from app import db` and `db.create_all()` as in local environment
- To inspect data use `heroku pg:psql` and for connecting via `pgadmin3`, follow [this](https://stackoverflow.com/a/11775090)
```
$ heroku pg:psql
--> Connecting to postgresql-wwwwwww-xxxxx
...
smariot::DATABASE=> \d
                List of relations
 Schema |    Name     |   Type   |     Owner      
--------+-------------+----------+----------------
 public | data        | table    | qatitgwoqpxhyp
 public | data_id_seq | sequence | qatitgwoqpxhyp
(2 rows)

smariot::DATABASE=> select * from data;
... DATA ...
smariot::DATABASE=> \q
```

### Useful SQL commands
```
DELETE FROM data WHERE timestamp < (CURRENT_TIMESTAMP - '60 minutes'::interval);
\COPY (SELECT * FROM data) TO '~/smariot/dump.txt';
TRUNCATE TABLE data;
```
