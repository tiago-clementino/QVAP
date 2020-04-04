from collections.abc import Iterable
from os import listdir

class SqlUtils:

    def just_logged(conn):
        if(conn and conn.connected()):
            #rows = conn.query("select name from sqlite_master where type = ?",('table',))#datetime(now)
            rows = conn.query("select logged, email from profile where logged = 1 order by last_login asc")#datetime(now)
            if(isinstance(rows, Iterable)):
                for row in rows:
                    if row[0] == 1:
                        result = conn.update('update profile set logged = 1, last_login = datetime(\'now\') where email = ?',(row[1],))
                        return row[1]
            else:
                print(rows)
            return None
        print('não conectado')
        return None

    def check_login(conn,login,password,msg=None):
        if(conn and conn.connected()):
            rows = conn.query("select * from profile where email = ? and password = ?",(login,password))
            if(isinstance(rows, Iterable)):
                if(len(rows) > 1):
                    print('Este login está duplicado:',login)
                elif(len(rows) == 0):
                    if(msg is not None):
                        msg.text = f'Login ou senha inválidos para este usuário: {login}'
                    else:
                        print('Login ou senha inválidos para este usuário:',login)
                    return False
                for row in rows:
                    result = conn.update('update profile set logged = 1, last_login = datetime(\'now\') where email = ?',(login,))
               
                    return (row[0],row[1])
            else:
                print(rows)
                if(msg is not None):
                    msg.text = 'Problemas com o banco de dados'
                return False
        
        if(msg is not None):
            msg.text = 'Não conectado ao banco de dados'
        else:
            print('Não conectado ao banco de dados')
        return False


    


    

    def record(conn,email,password,msg=None):
        message = ''
        if(conn and conn.connected()):
            if not SqlUtils.check_login(conn,email,password):
                result = conn.update("insert into profile(email,password,logged,last_login) values (?,?,1,datetime('now'))",(email,password))
                print(result)
                return True
                # if(isinstance(rows, Iterable)):
                #     if(len(rows) > 1):
                #         print('Este login está duplicado:',login)
                #     elif(len(rows) == 0):
                #         if(msg is not None):
                #             msg.text = f'Login ou senha inválidos para este usuário: {login}'
                #         else:
                #             print('Login ou senha inválidos para este usuário:',login)
                #         return False
                #     for row in rows:
                #         result = conn.update("update profile set logged = 1, last_login = datetime(now) where email = ?",(login,))
                #         return (row[0],row[1])
                # else:
                #     print(rows)
                #     if(msg is not None):
                #         msg.text = 'Problemas com o banco de dados'
                #     return False
            else:
                message = 'Esta usuário já está cadastrado'
        if message != '':
            if(msg is not None):
                msg.text = message
            else:
                print(message)
        return False




        
    

    def logoff(conn,email,msg=None):
        message = ''
        if(conn and conn.connected() and email is not None):
            result = conn.update("update profile set logged = 0 where email=?",(email,))
            if(type(result) == type(2)):
                
                return result >= 0
            else:
                return False
        if message != '':
            if(msg is not None):
                msg.text = message
            else:
                print(message)
        return False


                
