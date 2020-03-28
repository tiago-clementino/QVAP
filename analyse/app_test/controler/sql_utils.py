from collections.abc import Iterable
from os import listdir

class SqlUtils:

    def just_logged(conn):
        if(conn and conn.connected()):
            #rows = conn.query("select name from sqlite_master where type = ?",('table',))#datetime(now)
            rows = conn.query("select logged from profile where logged = 1 order by last_login asc")#datetime(now)
            if(isinstance(rows, Iterable)):
                for row in rows:
                    return row[0] == 1
            else:
                print(rows)
            return False
        print('não conectado')
        return False

    def check_login(conn,login,password,msg):
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
                    result = conn.update("update profile set logged = 1, last_login = datetime(now) where email = ?",(login,))
                    return (row[0],row[1])
            else:
                print(rows)
                if(msg is not None):
                    msg.text = f'Problemas com o banco de dados: {rows}'
                return False
        
        if(msg is not None):
            msg.text = f'Não conectado ao banco de dados: {listdir(".")}'
        else:
            print('Não conectado ao banco de dados')
        return False


                
