import sqlite3

# answer
# id | msg | answ
# Добавить несколько запросов ответов

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()

# query = """
# CREATE TABLE answer(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     msg TEXT,
#     answ TEXT
# )
# """
# cur.execute(query)
# conn.commit()

# query = """
# INSERT INTO answer(msg,answ) VALUES
# ("/start", 'Hello, there some commands you can use:\n
# 			1) /cheer [Чот забыл сделать😡]\n
# 			2) /dance\n
# 			3) /say [message]\n
# 			4) /myName\n
# 			5) /riddle'),
# ("/riddle", "Зимой и летом одним цветом")
# """
# cur.execute(query)
# conn.commit()

query = """
SELECT * FROM answer
"""
cur.execute(query)
print(cur.fetchall())

conn.commit()

conn.commit()
conn.close()