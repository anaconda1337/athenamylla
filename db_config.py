import sqlite3
import pandas as pd

#create db if doesn't exist
# def create_connection(users):
#     """ create a database connection to a SQLite database """
#     conn = None
#     try:
#         conn = sqlite3.connect(users)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()

#create db table
# connection_object = sqlite3.connect('users.db')

# cursor_obj = connection_object.cursor()

# table = """ CREATE TABLE USERS (
#             Username VARCHAR(255) NOT NULL,
#             User_FirstName VARCHAR(255) NOT NULL,
#             User_LastName VARCHAR(255) NOT NULL,
#             Chat_ID VARCHAR(255) NOT NULL
#             ); """
            
            
# cursor_obj.execute(table)

# print('table successfully created')

# connection_object.close()


#print everything * from the database
con = sqlite3.connect('users.db')
df = pd.read_sql_query("SELECT * from USERS", con)

print(df.head())

con.close()




