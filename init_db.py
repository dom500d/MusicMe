# Add the necessary imports
import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv

# Read Database connection variables

''' Environment Variables '''
load_dotenv()

db_host = os.getenv('MYSQL_HOST')
db_user = os.getenv('MYSQL_USER')
db_pass = os.getenv('MYSQL_PASSWORD')
db_name = os.getenv('MYSQL_DATABASE')



# Connect to the db and create a cursor object
db =mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()
cursor.execute('CREATE DATABASE if not exists onespot')
cursor.execute('USE onespot')
cursor.execute('drop table if exists users;')
try:
   cursor.execute('''
   CREATE TABLE users (
       user_id  integer  AUTO_INCREMENT PRIMARY KEY,
       username     VARCHAR(100) NOT NULL,
       password    varchar(100) not null    
   );
 ''')
except RuntimeError as err:
   print('runtime error: {0}'.format(err))

db.commit()
db.close()