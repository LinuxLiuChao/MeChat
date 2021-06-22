
import sqlite3


conn = sqlite3.connect("MeChat.db")
cursor = conn.cursor()

sql = open("./init.sql", "r").read()

cursor.execute(sql)

cursor.close()
conn.close()
