import sqlite3

# answer
# id | msg | answ

# db = sqlite3.connect('db.sqlite')
# cur = db.cursor()
# query = """
# CREATE TABLE answer(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     msg TEXT,
#     answ TEXT
# )
# """
# cur.execute(query)
# conn.commit()
# db.close()


def get(table_name, cols = "*"):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    "".format()

    query = """
        SELECT {1} FROM {0}
    """.format(table_name,  cols if cols=="*" else "({0})".format(",".join(cols)) )

    cur.execute(query)
    colNames = list(map(lambda x: x[0], cur.description))

    result = []

    for i in cur.fetchall():
        result.append(dict(zip(colNames, i)))
    db.close()

    return result

def insert(table_name, cols, data):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    query = """
        INSERT INTO {0}({1})
        VALUES('{2}');
    """.format(table_name, ",".join(cols), "','".join(data))

    cur.execute(query)

    db.commit()
    db.close()



##Создать таблицу group


# db = sqlite3.connect('db.sqlite')
# cur = db.cursor()

# query1 = """
# CREATE TABLE groups(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     groupName TEXT
# )
# """

# query2 = """
# CREATE TABLE user(
#     id INTEGER PRIMARY KEY,
#     groupId INTEGER, 
    
    
#     FOREIGN KEY (groupId) REFERENCE groups (id)
# )
# """

# cur.execute(query1)
# db.commit()
# cur.execute(query2)
# db.commit()

# db.close()

# insert("groups", ["groupName"], ["Администратор"])
# insert("groups", ["groupName"], ["Наставник"])
# insert("groups", ["groupName"], ["Ученик"])

# print(get("groups"))