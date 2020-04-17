from kivy.uix.screenmanager import Screen
from controler.connect_sqlite import Connection
from screens.login import Login

class Recents(Screen):

    def build(self):
        super(Recents, self)

    def __init__(self):
        super(Recents, self).__init__()    
    
    def logoff(self,msg=None):
        if Login.logoff(msg):
            self.manager.transition.direction = 'right'
            self.manager.current = 'login'

    @staticmethod
    def format_message(msg):
        return f'"[color=222222][b]{msg}[/b][/color]"'

    def clear_message(self, msg):
        if(msg is not None):
            msg.text = ''