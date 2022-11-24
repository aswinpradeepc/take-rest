import mysql.connector
import os
import datetime as dt
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv('LOCAL_HOST'),
  user=os.getenv('USER'),
  password=os.getenv('PASSWORD'),
  database=os.getenv('DATABASE')
)

cursor = mydb.cursor()

def insert(blink_count):
    t = dt.datetime.now()
    cursor.execute(f"INSERT INTO BLINK (blinked_at, blink_count) VALUES('{t.strftime('%Y-%m-%d %H:%M:%S')}',{blink_count});")
    mydb.commit()

def fetch():
    cursor.execute("SELECT * FROM BLINK;")
    myresult = cursor.fetchall()
    print(myresult)
    return myresult



#call the function insert() and pass the value of blink count to insert to database.
#call the function fetch() to get the details of all records in database.