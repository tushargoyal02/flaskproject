import mysql.connector

def connection():
    conn = mysql.connector.connect(host='localhost',database='flaskproject',user='root',password='  l')

    cur = conn.cursor
    return cur,conn