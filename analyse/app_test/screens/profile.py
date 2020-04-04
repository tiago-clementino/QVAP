from kivy.uix.screenmanager import Screen
from screens.login import Login

class Profile(Screen):

    instance = None
    
    def build(self):
        super(Profile, self)
        Profile.set_instance(self)

    def __init__(self):
        super(Profile, self).__init__()

    @staticmethod
    def get_instance():
        if(Profile.instance == None):
            Profile.instance = Profile()
        return Profile.instance

    @staticmethod
    def set_instance(instance):
        if(Profile.instance == None):
            Profile.instance = instance

    def get_audience(self):
        return 0

    def get_total_results(self):
        return 10

    def clear_message(self, msg):
        if(msg is not None):
            msg.text = ''

    def set_all(self, grid, msg):
        self.clear_message(msg)
        if(grid is not None):
            for xx in grid.children:
                if(xx.name == 'email'):
                    xx.text = Login.email
    
    def logoff(self,msg=None):
        if Login.logoff(msg):
            self.manager.transition.direction = 'right'
            self.manager.current = 'login'