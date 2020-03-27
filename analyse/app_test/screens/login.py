from kivy.uix.screenmanager import Screen
from controler.connect_sqlite import Connection
from controler.sql_utils import SqlUtils
from pathlib import Path

class Login(Screen):

    conn = None

    def build(self):
        super(Login, self)

    def __init__(self):
        super(Login, self).__init__()
        self.conn = Connection()
        self.conn.create_connection()#Path("data/") / "database.db")

    def check_login(self,login=None,password=None,msg=None):
        if login is not None and password is not None and login.text.strip() != '' and password.text.strip() != '':
            if SqlUtils.check_login(self.conn,login.text,password.text,msg):
                self.manager.transition.direction = 'left'
                self.manager.current = 'recents'
            # else:
            #     msg.text = 'Login inválido'
        else:
            msg.text = 'Login inválido'
            #return 'Login inválido'

    def just_logged(conn):
        return SqlUtils.just_logged(conn)
        
    def get_connection(self):
        return self.conn
        