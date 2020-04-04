from pandas import DataFrame
from pandas import read_json
from screens.profile import Profile
from pathlib import Path

class Qvap:

    male_age_1 = 0
    male_age_2 = 1
    female_age_1 = 2
    female_age_2 = 3
    age_1 = 4
    age_2 = 5
    male = 6
    female = 7
    all_ = 8

    paths = [r'all.zip',r'male_age_1.zip',r'female_age_1.zip',r'male_age_2.zip',r'female_age_2.zip',r'age_1.zip',r'age_2.zip',r'male.zip',r'female.zip']

    current_model = None
    current_packagings = None
    current_path = None


    atributes=['Material','Forma','Cor','Constituição','Superfície']
    atributes_en=['material','shape','color','constitution','surface']
    translated_atributes_en={'material':'Material','shape':'Forma','color':'Cor','constitution':'Constituição','surface':'Superfície'}
    translated_atributes={'Material':'material','Forma':'shape','Cor':'color','Constituição':'constitution','Superfície':'surface'}
    atribute_variances={'Material':['Papel Cartão','Metal','Polímero','Vidro'],'Cor':['Neutra','Intensa'],'Superfície':['Brilhosa','Fosca'],'Forma':['Orgânica','Geométrica'],'Constituição':['Ordem','Complexidade']}

    def __init__(self):
        pass

    @staticmethod
    def get_atributes():
        return Qvap.atributes

    @staticmethod
    def get_atributes_en():
        return Qvap.atributes_en

    @staticmethod
    def translate_atributes(atribute):
        return Qvap.translated_atributes[atribute]

    @staticmethod
    def translate_atributes_en(atribute):
        return Qvap.translated_atributes_en[atribute]

    @staticmethod
    def image_path(name_path):
        return f'images/png/{name_path}.gif'

    @staticmethod
    def get_image_name(atribute_variances):
        if(atribute_variances is None):
            return Qvap.image_path('XG')
        name = ''
        right_atributes = Qvap.get_atributes()
        for v in right_atributes:
            for xx in Qvap.atribute_variances[v]:
                for yy in atribute_variances:
                    if(yy in xx):
                        name = f'{name}{Qvap.get_atribute_letter(yy)}'
    
        if(len(name) == 0):
            return 'XG'
        return Qvap.image_path(name)


    @staticmethod
    def get_atribute_letter(v):
        if(v == Qvap.atribute_variances['Material'][0]):
            return 'X'
        if(v is None or len(v) == 0):
            return ''
        return v[0].upper()

    @staticmethod
    def is_mandatory_atribute_picture(atribute):
        if(atribute == Qvap.atributes[1]):
            return True
        elif(atribute == Qvap.atributes[0]):
            return True

    @staticmethod
    def get_mandatory_atribute_picture(atribute):
        if(atribute == Qvap.atributes[1]):
            return Qvap.get_atribute_letter(Qvap.atribute_variances[atribute][1])
        elif(atribute == Qvap.atributes[0]):
            return Qvap.get_atribute_letter(Qvap.atribute_variances[atribute][0])


    @staticmethod
    def is_condictional_atribute_picture(atribute):
        if(atribute == Qvap.atributes[4]):
            return True

    @staticmethod
    def get_condictional_atribute_picture(atribute):
        if(atribute == Qvap.atributes[4]):
            return Qvap.atributes[2]

    @staticmethod
    def get_condictional_variance_picture(atribute):
        if(atribute == Qvap.atributes[2]):
            return Qvap.get_atribute_letter(Qvap.atribute_variances[Qvap.atributes[2]][0])


    @staticmethod
    def get_variances(atribute):
        if(atribute != None and atribute in Qvap.atributes):
            return Qvap.atribute_variances[atribute]
        return None

    @staticmethod
    def create_model_2(path=None):

        if(path is None):
            path = Profile.get_instance().get_audience()

        if(path is not None and path < len(Qvap.paths) and path >= 0 and Qvap.current_path != path):
            Qvap.current_path = path
            
            #Qvap.current_model = read_json(Path("json/") / f'model_{Qvap.paths[path]}', compression='zip', orient='columns')
            Qvap.current_packagings = read_json(Path("json/") / f'packagings_{Qvap.paths[path]}', compression='zip', orient='columns')
        elif(Qvap.current_path is None):
            print('Modelo desconhecido')
            return None
        return Qvap.current_packagings#, Qvap.current_model

    @staticmethod
    def create_model(path=None):

        if(path is None):
            path = Profile.get_instance().get_audience()

        if(path is not None and path < len(Qvap.paths) and path >= 0 and Qvap.current_path != path):
            Qvap.current_path = path
            
            Qvap.current_model = read_json(Path("json/") / f'model_{Qvap.paths[path]}', compression='zip', orient='columns')
            Qvap.current_packagings = read_json(Path("json/") / f'packagings_{Qvap.paths[path]}', compression='zip', orient='columns')
        elif(Qvap.current_path is None):
            print('Modelo desconhecido')
            return None
        elif(Qvap.current_model is None):
            Qvap.current_model = read_json(Path("json/") / f'model_{Qvap.paths[Qvap.current_path]}', compression='zip', orient='columns')
        return Qvap.current_packagings, Qvap.current_model

    @staticmethod
    def get_matched_packaging(fixed_attributes, fixes, model_path=None):
        '''retorna uma tupla contendo de um lado as embalagens isoladas e do outro as embalagens em todas as comparações possíveis
            fixed_attributes: atributos em si
            fixes: variações de atributos
        '''
        packagings, model = Qvap.create_model(model_path)
        right_packagings = packagings
        for i in range(len(fixed_attributes)):
            right_packagings = right_packagings.loc[right_packagings[Qvap.translate_atributes(fixed_attributes[i])] == fixes[i]]

        #isto aqui ficou aloprado por conta do formato nada funcional do JSON
        #seleciona todas as URLs compatíveis com as restrições (right_packagings) nas tuplas do modelo (model)
        right_model = model.loc[  [[any(z[v]==xx for xx in right_packagings['URL']) for v in z][0] for z in model['URL_most']]    ]

        right_model.loc[:,'URL_most'] =  [[z[v] for v in z][0] for z in right_model['URL_most']]
        right_model.loc[:,'URL_less'] =  [[z[v] for v in z][0] for z in right_model['URL_less']]

        right_model.set_index(['URL_most','URL_less'],drop=True,inplace=True)

        return right_packagings, right_model

    @staticmethod
    def get_matched_packaging_2(fixed_attributes, fixes, model_path=None):
        '''retorna as embalagens isoladas
            fixed_attributes: atributos em si
            fixes: variações de atributos
        '''
        packagings = Qvap.create_model_2(model_path)
        right_packagings = packagings
        for i in range(len(fixed_attributes)):
            right_packagings = right_packagings.loc[right_packagings[Qvap.translate_atributes(fixed_attributes[i])] == fixes[i]]

        return right_packagings

    @staticmethod
    def get_matched_packaging_3(fixed_attributes, fixes, variable_attributes, variances, model_path=None):
        '''retorna as embalagens isoladas
            fixed_attributes: atributos em si
            fixes: variações de atributos
        '''
        packagings = Qvap.create_model_2(model_path)
        right_packagings = packagings
        if(fixed_attributes is not None):
            for i in range(len(fixed_attributes)):
                right_packagings = right_packagings.loc[right_packagings[Qvap.translate_atributes(fixed_attributes[i])] == fixes[i]]
        if(variable_attributes is not None):
            for j in range(len(variable_attributes)):
                right_packagings = right_packagings.loc[right_packagings[Qvap.translate_atributes(variable_attributes[j])] != variances[j]]

        return right_packagings


    @staticmethod
    def get_best_distinct_settings_2(fixed_attributes, fixes, variable_attributes, variances, model_path=None, msg=None):

        #listas
        #packagins devem ter as pontuações para cada embalagem e  médias de influência por atributo
        #matches devem ser o que são, mas indexadas pela URL da embalagem (que deve constar em packagins)
        #packagings, matches = Qvap.get_matched_packaging_2(fixed_attributes, fixes, model_path)
        #packagings = Qvap.get_matched_packaging_2(fixed_attributes, fixes, model_path)
        
        packagings = Qvap.get_matched_packaging_3(fixed_attributes, fixes, variable_attributes, variances, model_path)

        # packagings.reset_index(drop=True,inplace=True)

        # print(3)

        # #algoritmo bublesort para garantir que todos sejam comparados com todos (comparações podem ser imprecisas)
        # for i in range(len(packagings)):
        #     for j in range(len(packagings)-1):
        #         #if matches[packagings[j]['URL'],packagings[j+1]['URL']]['true'] > 0.5:
        #         if((packagings.loc[j].at['URL'],packagings.loc[j+1].at['URL']) in matches.index):
        #             #print(matches[(packagings.loc[j].at['URL'],packagings.loc[j+1].at['URL'])])
        #             #if matches[(packagings.loc[j].at['URL'],packagings.loc[j+1].at['URL'])]['true'] > 0.5:
        #             #print(matches.loc[(packagings.loc[j].at['URL'],packagings.loc[j+1].at['URL'])])
        #             if matches.loc[(packagings.loc[j].at['URL'],packagings.loc[j+1].at['URL'])]['verdadeiro'] > 0.5:
        #                 temp = packagings.loc[j]
        #                 packagings.loc[j] = packagings.loc[j+1]
        #                 packagings.loc[j+1] = temp
        
        # print(4)
        return packagings.sort_values(by=['score'], ascending=False)[:10].reset_index()#10 deve ser flexível e constar em settigns (base de dados)

