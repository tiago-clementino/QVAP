from kivy.uix.screenmanager import Screen
from controler.connect_sqlite import Connection
from controler.sql_utils import SqlUtils
from pathlib import Path

class Login(Screen):

    conn = None
    email = None

    def build(self):
        super(Login, self)

    def __init__(self, datapath = None):
        super(Login, self).__init__()
        Login.conn = Login.get_connection(datapath)
        #Login.conn = Connection()
        #Login.conn.create_connection()#Path("data/") / "database.db")

    @staticmethod
    def new_connection(datapath = None):
        Login.conn = Connection()
        Login.conn.create_connection()#Path("data/") / "database.db")

    
    @staticmethod
    def format_message(msg):
        return f'"[color=222222][b][/b]{msg}[/color]"'

    def check_login(self,login=None,password=None,msg=None):
        if login is not None and password is not None and login.text.strip() != '' and password.text.strip() != '':
            if SqlUtils.check_login(Login.get_connection(),login.text,password.text,msg):
                Login.set_login(login.text)
                self.manager.transition.direction = 'left'
                self.manager.current = 'recents'
            # else:
            #     msg.text = 'Login inválido'
        else:
            msg.text = Login.format_message( 'Login inválido') 
            #return 'Login inválido'

    @staticmethod
    def just_logged(conn):
        login = SqlUtils.just_logged(conn)
        Login.set_login(login)
        return login is not None

    @staticmethod
    def set_login(login):
        if(login is not None and login != ''):
            Login.email=login


    @staticmethod
    def logoff(msg=None):
        if SqlUtils.logoff(Login.get_connection(),Login.email,msg) > 0:
            Login.email=None
            return True
        return False


    # @staticmethod
    # def logoff(msg=None):
    #     if Login.logoff_2(msg):
    #         self.manager.transition.direction = 'right'
    #         self.manager.current = 'login'
        
    @staticmethod
    def get_connection(datapath = None):
        if(Login.conn == None or not Login.conn.connected()):
            Login.new_connection(datapath)
        return Login.conn

    @staticmethod
    def close_connection():
        if(Login.conn != None and Login.conn.connected()):
            Login.conn.close_connection()

        