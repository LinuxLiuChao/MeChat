
import sqlite3


conn = sqlite3.connect("MeChat.db")
cursor = conn.cursor()

sql = open("./sqlite3_init.sql", "r").read()

cursor.executescript(sql)

cursor.close()
conn.close()
