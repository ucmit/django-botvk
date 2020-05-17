import sqlite3




def get(table_name, cols = "*"):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    query = """
        SELECT {1} FROM {0}
        """.format(table_name,  cols if cols=="*" else "({0})".format(",".join(cols)))

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

def getGroup(userID = None):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    query = ""

    if userID == None:
        query = """
            SELECT * FROM groups
            JOIN user
            ON groups.id = user.groupId
        """
    else:
        query = """
            SELECT * FROM groups
            INNER JOIN user
            ON groups.id = user.groupId
            WHERE user.id == '{0}'
        """.format(userID) 

    cur.execute(query)
    colNames = list(map(lambda x: x[0], cur.description))

    result = []

    for i in cur.fetchall():
        result.append(dict(zip(colNames, i)))
    db.commit()
    db.close()

    return result

def deleteUser(userID = None):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    if(getGroup(userID)) == []:
        db.commit()
        db.close()
        return "Ошибка, такого пользователя нет в Базе Данных"

    query = ""

    if userID == None:
        query = """
            DELETE FROM user
        """
    else:
        query = """
            DELETE FROM user
            WHERE user.id == '{0}'
        """.format(userID)
    
    cur.execute(query)
    db.commit()
    db.close()

    return "Вы были удалены из базы данных"

# ====================
# answer
# id | msg | answ

# db = sqlite3.connect('db.sqlite')
# cur = db.cursor()

# query0 = """
# CREATE TABLE answer(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     msg TEXT,
#     answ TEXT
# )
# """

# ====================
# groups
# id | groupName

# query1 = """
# CREATE TABLE groups(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     groupName TEXT
# )
# """

# ====================
# user
# id | groupId

# query2 = """
# CREATE TABLE user(
#     id INTEGER PRIMARY KEY,
#     groupId INTEGER, 
     
#     FOREIGN KEY (groupId) REFERENCES groups(id)
# )
# """

# cur.execute(query0)
# conn.commit()

# cur.execute(query1)
# conn.commit()

# cur.execute(query2)
# conn.commit()

# db.close()

# ====================
# insert("groups", ["groupName"], ["Администратор"])
# insert("groups", ["groupName"], ["Наставник"])
# insert("groups", ["groupName"], ["Ученик"])