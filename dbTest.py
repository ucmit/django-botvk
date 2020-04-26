import sqlite3

# Создать таблицу cars
# id | mark | color | number|
# Добавить 5 машин, и вывести на экран через result

# Подключаемся к нашей базе данных
conn = sqlite3.connect('db.sqlite')
# Создаём курсор для нашего подключения
cur = conn.cursor()

# Запрос для создание таблицы 
# query = """
# CREATE TABLE phonebook(
#     id INT PRIMARY KEY,
#     name TEXT,
#     p_number INT
# );
# """

# Запрос на добавление значений в таблицу
# query = """
# INSERT INTO phonebook (id, name, p_number) VALUES 
# (1, 'Артек', 8800553535),
# (2, 'Жорик', 8800553535),
# (3, 'Максик', 8800553535),
# (4, 'Лерой', 8800553535),
# (5, 'Борис', 8800553535);
# """
# Запрос на добавление значения в таблицу
# query = """
# INSERT INTO phonebook (id, name, p_number) VALUES (1, 'Артек', 8800553535);
# """

# Запрос для выборки значений таблицы
query = """
SELECT * FROM phonebook
"""

# Выполняем запрос через курсор
cur.execute(query)

result = cur.fetchall()
print(result)
# Сохраняем состояние бд
conn.commit()


# Закрываем подключени к БД
conn.close()