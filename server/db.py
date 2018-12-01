# import sqlite3


# def reset_db():
#     conn = sqlite3.connect('database.db')
#     conn.execute('DROP TABLE users')

# def init_db():
#     conn = sqlite3.connect('database.db')
#     print ("Opened database successfully")

#     conn.execute('CREATE TABLE users (id TEXT, name TEXT)')
#     print ("Table created successfully");

# def insert_user(id, name):
#     with sqlite3.connect("database.db") as con:
#         try:
#             cur = con.cursor()
#             cur.execute("INSERT INTO users (id,name) VALUES (?,?)",(id, name) )
#             con.commit()
#             msg = "Record successfully added"
#         except:            
#             con.rollback()
#             msg = "error in insert operation"

# def get_user(id):
#     with sqlite3.connect("database.db") as con:
#         con.row_factory = sqlite3.Row
#         cur = con.cursor()
#         cur.execute('SELECT * FROM users WHERE id=?', (id,))
#         row = cur.fetchone()
#         if row is None:
#             return None
#     return dict(row)


# def close_db():
#     conn.close()

# reset_db()
# init_db()
# insert_user("hello", "Alex")
# print(get_user("hello"))


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

