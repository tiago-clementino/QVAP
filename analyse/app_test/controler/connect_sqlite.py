import sqlite3
from sqlite3 import Error
from pathlib import Path

class Connection:

    conn = None
    def __init__(self):
        self.path_name = Path("data/") / "database.db"

    def create_connection(self, path_name=None):
        """ create a database connection to a SQLite database """
        conn = None
        print(path_name)
        try:
            if(path_name is None):
                self.conn = sqlite3.connect(self.path_name.__str__())
            else:
                self.conn = sqlite3.connect(path_name.__str__())
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if self.connected() and path_name is not None:
                self.path_name = path_name
        # finally:
        #     if conn:
        #         conn.close()

    def connected(self):
        if self.conn:
            return True
        return False

    def close_connect(self):
        if self.connected():
            self.conn.close()

    def query(self,sql,values=None):
        '''Values é uma tupla'''
        try:
            if self.conn:
                cur = self.conn.cursor()
                if(values is None):
                    cur.execute(sql)
                else:
                    cur.execute(sql,values)
                rows = cur.fetchall()
                cur.close
                return rows
            else:
                return 'Falha na conexão com o banco de dados 1'
        except Error as e:
            return e
        
    def update(self,sql,values=None):
        '''Values é uma tupla'''
        try:
            if self.conn:
                cur = self.conn.cursor()
                if(values is None):
                    cur.execute(sql)
                else:
                    cur.execute(sql,values)
                result = cur.commit()
                cur.close
                return result
            else:
                return 'Falha na conexão com o banco de dados 2'
        except Error as e:
            return e