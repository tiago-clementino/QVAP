from kivy.uix.screenmanager import Screen
from controler.sql_utils import SqlUtils
from screens.login import Login

class Logup(Screen):

    def build(self):
        super(Logup, self)

    def __init__(self):
        super(Logup, self).__init__()

    def record(self,email,password,confirm_password,msg=None):
        if self.check_email_format(email,msg) and self.check_password_format(password,confirm_password,msg):
            if SqlUtils.record(Login.get_connection(),email.text,password.text,msg):
                self.manager.transition.direction = 'left'
                self.manager.current = 'recents'

    def check_password_format(self,password,confirm_password,msg=None):
        message = ''
        if password is not None and confirm_password is not None:
            if password.text.strip() != '' and confirm_password.text.strip() != '':
                if len(password.text) > 4:
                    if password.text == confirm_password.text:
                        return True
                    else:
                        message = 'Senha e confirmação de senha não conferem'
                else:
                    message = 'Senha deve ter mais de 4 caracteres'
            else:
                message = 'Senha não pode ter apenas espaços em branco'
        else:
            message = 'Senha ou confirmação de senha não informada'
        if message != '':
            if(msg is not None):
                msg.text = message
            else:
                print(message)
        return False


    def check_email_format(self,email,msg=None):
        message = ''
        if email is not None:
            email = email.text.strip()
            email_find = email.find('@')
            if email_find > 0 and email_find < len(email)-1:
                return True
            else:
                message = 'E-mail mal formatado, verifique'
        else:
            message = 'E-mail não informado'
        if message != '':
            if(msg is not None):
                msg.text = message
            else:
                print(message)
        return False