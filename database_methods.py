import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Conection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection,query):
    cursor=connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error {e} has occurred")

def read_query(connection, query):
    cursor=connection.cursor()
    result=None
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        return result
    except Error as e:
        print (f"The error '{e}' occurred")

create_login_table = f"CREATE TABLE IF NOT EXISTS login (\
    id INTEGER PRIMARY KEY AUTOINCREMENT,\
    username TEXT NOT NULL UNIQUE,\
    password TEXT NOT NULL, \
    security_question TEXT NOT NULL, \
    security_answer TEXT NOT NULL, \
    expense REAL NOT NULL,\
    income REAL NOT NULL,\
    FOREIGN KEY (expense) REFERENCES expenses(total))"

def username_table(connection,x):
    create_username_table=f"CREATE TABLE IF NOT EXISTS '{x}'(\
    id INTEGER PRIMARY KEY AUTOINCREMENT, AMOUNT REAL NOT NULL,\
    CATEGORY TEXT, DESCRIPTION TEXT, DATE TEXT)"
    execute_query(connection,create_username_table)

connection=create_connection("mydatabase.db")
execute_query(connection,create_login_table)
