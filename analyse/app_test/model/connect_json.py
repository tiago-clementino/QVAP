from pandas import DataFrame
from pandas import read_json

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

    paths = [r'all.json',r'male_age_1.json',r'female_age_1.json',r'male_age_2.json',r'female_age_2.json',r'age_1.json',r'age_2.json',r'male.json',r'female.json']

    current_model = None
    current_packagings = None
    current_path = None


    atributes=['Material','Forma','Cor','Constituição','Superfície']
    atribute_variances={'Material':['Papel Cartão','Metal','Polímero','Vidro'],'Cor':['Neutra','Intensa'],'Superfície':['Brilhosa','Fosca'],'Forma':['Orgânica','Geométrica'],'Constituição':['Ordem','Complexidade']}

    def __init__(self):
        pass

    @staticmethod
    def get_atributes():
        return Qvap.atributes

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
    def create_model(path=None):

        if(path is not None and path < len(Qvap.paths) and path >= 0 and Qvap.current_path != path):
            Qvap.current_path = path
            Qvap.current_model = read_json(Path("json/") / Qvap.paths[f'model_{path}'])
            Qvap.current_packagings = read_json(Path("json/") / Qvap.paths[f'packagins_{path}'])
        elif(Qvap.current_path is None):
            pritn('Modelo desconhecido')
            return None
        return current_packagings, Qvap.current_model

    @staticmethod
    def get_matched_packaging(fixed_attributes, fixes, model_path=None):
        '''retorna uma tupla contendo de um lado as embalagens isoladas e do outro as embalagens em todas as comparações possíveis'''
        packagings, model = Qvap.create_model(model_path)
        right_packagings = packagings
        for i in range(len(fixed_attributes)):
            right_packagings = right_packagings.loc[right_packagings[fixed_attributes[i]] == fixes[i]]
        right_model = model.loc[right_model['URL_most'] in right_packagings['URL']]
        return right_packagings, right_model


    @staticmethod
    def get_best_distinct_settings_2(fixed_attributes, fixes, variable_attributes, variances, model_path=None):

        #listas
        #packagins devem ter as pontuações para cada embalagem e  médias de influência por atributo
        #matches devem ser o que são, mas indexadas pela URL da embalagem (que deve constar em packagins)
        packagings, matches = get_matched_packaging(fixed_attributes, fixes, model_path)

        #algoritmo bublesort para garantir que todos sejam comparados com todos (comparações podem ser imprecisas)
        for i in range(len(packagings)):
            for j in range(len(packagings)-1):
                if matches[packagings[j]['URL'],packagings[j+1]['URL']]['true'] > 0.5:
                    temp = packagings[j]
                    packagings[j] = packagings[j+1]
                    packagings[j+1] = temp

        return packagings[:10]#10 deve ser flexível e constar em settigns (base de dados)

