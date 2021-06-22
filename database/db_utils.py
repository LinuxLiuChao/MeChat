import sqlite3


conn = sqlite3.connect("MeChat.db")
cursor = conn.cursor()

sql = "select * from user;"

cursor.execute(sql)
ret = cursor.fetchall()
print(f"{ret}")

cursor.close()
conn.close()
