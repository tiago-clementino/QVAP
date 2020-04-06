from collections.abc import Iterable
from os import listdir

class SqlUtils:

    
    @staticmethod
    def format_message(msg):
        return f'"[color=222222][b][/b]{msg}[/color]"'

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

    

    def create_model(conn,fixed_attributes, variable_attributes, msg=None):
        if(conn and conn.connected()):
                
            sql_sufix = "select * from packaging"
            sql = ""
            tuple_ = []#tuple()
            if(fixed_attributes is not None):
                
                for i,v in fixed_attributes.items():
                    if(sql != ''):
                        sql = f'{sql} and '
                    sql = f'{sql}{i} = ?'
                    tuple_.append(v)
                    
            if(variable_attributes is not None):
                
                for i,v in variable_attributes.items():
                    if(sql != ''):
                        sql = f'{sql} and '
                    sql = f'{sql}{i} <> ?'
                    tuple_.append(v)

            if(sql != ''):
                sql = f'{sql_sufix} where {sql} order by score desc LIMIT 10'
            else:
                sql = f'{sql_sufix} order by score desc LIMIT 10'

            rows = conn.query(sql,tuple_)
            return rows
            
        return None

    def check_login(conn,login,password,msg=None):
        if(conn and conn.connected()):
            rows = conn.query("select * from profile where email = ? and password = ?",(login,password))
            if(isinstance(rows, Iterable)):
                if(len(rows) > 1):
                    print('Este login está duplicado:',login)
                elif(len(rows) == 0):
                    if(msg is not None):
                        msg.text = SqlUtils.format_message(f'Login ou senha inválidos para este usuário: {login}')     
                    else:
                        print('Login ou senha inválidos para este usuário:',login)
                    return False
                for row in rows:
                    result = conn.update('update profile set logged = 1, last_login = datetime(\'now\') where email = ?',(login,))
               
                    return (row[0],row[1])
            else:
                print(rows)
                if(msg is not None):
                    msg.text = SqlUtils.format_message( 'Problemas com o banco de dados')  
                return False
        
        if(msg is not None):
            msg.text = SqlUtils.format_message('Não conectado ao banco de dados')  
        else:
            print('Não conectado ao banco de dados')
        return False


    

    

    def create_packagings(conn,packagings):
        if packagings is not None:
            if(conn and conn.connected()):
                result = dict()
                for i,v in packagings['URL'].items():
                    URL = v
                    score = packagings['score'][i]
                    material = packagings['material'][i]
                    material_weight = packagings['material_weight'][i]
                    shape = packagings['shape'][i]
                    shape_weight = packagings['shape_weight'][i]
                    color = packagings['color'][i]
                    color_weight = packagings['color_weight'][i]
                    constitution = packagings['constitution'][i]
                    constitution_weight = packagings['constitution_weight'][i]
                    surface = packagings['surface'][i]
                    surface_weight = packagings['surface_weight'][i]

                    result[i] = conn.update("insert into packaging(URL,score,material,material_weight,shape,shape_weight,color,color_weight,constitution,constitution_weight,surface,surface_weight) values (?,?,?,?,?,?,?,?,?,?,?,?)",(URL,score,material,material_weight,shape,shape_weight,color,color_weight,constitution,constitution_weight,surface,surface_weight))
                return result
        return None



    

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


                
