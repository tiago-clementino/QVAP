from kivy.uix.screenmanager import Screen
from screens.login import Login
from controler.connect_sqlite import Connection

class Recents(Screen):

    def build(self):
        super(Recents, self)

    def __init__(self):
        super(Recents, self).__init__()    

    def logoff(self,msg=None):
        if Login.logoff(msg):
            self.manager.transition.direction = 'right'
            self.manager.current = 'login'