We have built a Flask Application using RESTful API - Error Handling, Authentication.

Team Members:
Devashri Manepatil (885185645)
Apoorva Machale (885209536)

1. Setup Virtual Env using command: virtualenv -p python3 myvenv
3. Activate the virutal env using command: source myvenv/bin/activate
4. Install the packages mentioned in the requirements.txt: pip freeze > requirements.txt
5. In Mysql create database "stress_detection_data"
6. Create 2 schemas named users and user_schedule:

CREATE TABLE IF NOT EXISTS users ( user_id int NOT NULL AUTO_INCREMENT, email varchar(100) NOT NULL, password varchar(255) NOT NULL, PRIMARY KEY (user_id) ) ENGINE=InnODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS user_schedule ( user_id int NOT NULL AUTO_INCREMENT, name varchar(50) NOT NULL, email varchar(100) NOT NULL,exercise varchar(100) NOT NULL, number_busy_week_days integer(10) NOT NULL, weekend_activity varchar(100) NOT NULL, PRIMARY KEY (user_id) ) ENGINE=InnODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

7. Make requirements changes in the app.py with the username and password for your database installed on your machine.
8. Change the upload path in app.py based on the PATH you have on your computer to make use of upload API.


