import mysql.connector
import pymysql
def connection():
    conn = pymysql.connect(host='localhost',database='flaskproject',user='root',password='  l')
    c = conn.cursor()
    return c,conn