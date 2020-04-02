
import pandas as pd
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from functools import partial
from kivy.uix.spinner import SpinnerOption
from model.connect_json import Qvap
from widgets.my_spinner import SpinnerWidget
from widgets.my_spinner import SpinnerOptions

class New(Screen):

    atribute_list_fixed = None
    atribute_list_unwished = None

    background_color_fixed = [2.8, 2.8, 2.8, 1]
    background_color_unwished = [7, 2, 2, 1]

    changing_image = None

    def __init__(self):
        
        super(New, self).__init__()   
        self.atribute_list_fixed = pd.DataFrame([],columns=['atributo','valor'])
        self.atribute_list_fixed.set_index('atributo',inplace=True)
        self.atribute_list_unwished = pd.DataFrame([],columns=['atributo','valor'])
        self.atribute_list_unwished.set_index('atributo',inplace=True)
    
    def change_image(self):
        if(self.changing_image is not None):
            image_name = ''
            # material - forma - cor - const - super
            atributes = Qvap.get_atributes()

            current_atributes = []
            #current_variances = []
            for v in atributes:
                if(v in self.atribute_list_fixed.index):
                    current_atributes.append(v)
                    #current_variances.append(self.atribute_list_fixed.loc[v].values[0])
                    if(Qvap.is_condictional_atribute_picture(v)):
                        current_atributes.append(Qvap.get_condictional_atribute_picture(v))
                        #current_variances.append(Qvap.get_condictional_variance_picture(v))

            print(current_atributes)
            for v in atributes:
                #if(v in self.atribute_list_fixed.index):
                if(v in current_atributes):
                    if(v in self.atribute_list_fixed.index):
                        image_name = f'{image_name}{Qvap.get_atribute_letter(self.atribute_list_fixed.loc[v].values[0])}'
                    else:
                        print(v)
                        image_name = f'{image_name}{Qvap.get_atribute_letter(Qvap.get_condictional_variance_picture(v))}'
                    

                elif(Qvap.is_mandatory_atribute_picture(v)):
                    image_name = f'{image_name}{Qvap.get_mandatory_atribute_picture(v)}'

            print(image_name)
            self.changing_image.source = f'images/png/{image_name}.png'
    
    def spinner_clicked(self, changing_image, grid, classname, default_text):
        self.changing_image = changing_image
        self.add_year(grid, classname, default_text)
    
    def get_atributes(self):
        return Qvap.get_atributes()
    
    def add_year(self, grid, classname, default_text):
        
        if(classname.text == default_text):
            return

        my_text = SpinnerOptions.format_out(classname.text)


        """ The values of this spinner are temporary, I don't know how to insert other child spinners inside
        I think I must replace the spinner by a Drop Down but I can't do it, I need some help"""
        background = self.background_color_fixed
        print(my_text,self.atribute_list_unwished)
        print(my_text,self.atribute_list_fixed)
        if(default_text.find('Indesejáveis')>= 0):
            background = self.background_color_unwished
            if my_text in self.atribute_list_unwished.index or my_text in self.atribute_list_fixed.index:
                classname.text = default_text
                return
            self.atribute_list_unwished=self.atribute_list_unwished.append(pd.DataFrame([''],index=[my_text],columns=self.atribute_list_unwished.columns))
        else:
            if my_text in self.atribute_list_fixed.index:
                classname.text = default_text
                return
            self.atribute_list_fixed=self.atribute_list_fixed.append(pd.DataFrame([''],index=[my_text],columns=self.atribute_list_fixed.columns))
            

        
        #atribute_variances = [f'{classname.text}={x}' for x in Qvap.get_variances(classname.text)]
        atribute_variances = Qvap.get_variances(my_text)
        if(atribute_variances is None):
            classname.text = default_text
            return
        #left = Spinner(values = ["?", "??", "???"], text=classname.text, size = (32, 32), size_hint = (1, None))
        left = SpinnerWidget(values = atribute_variances, text=New.layout(my_text), markup=True, background_color=background, height = 32, size_hint = (1, None))


        aux = left.text

        # the delete button of this year
        right = Button(background_color = (2,0,0,1), text="X", size = (32, 32), size_hint = (None, None))
        
        left.bind(text=partial(self.set_atribute_variance, grid, left, right, aux) )#lambda *args: self.set_atribute_variance(aux, args))

        # equivalent of: on_press = self.del_year(grid, left, right) without NoneType error
        right.bind(on_press=partial(self.del_year, grid, left, right))

        # add these 2 buttons to the GridLayout
        grid.add_widget(left)
        grid.add_widget(right)
        # clear bottom's TextInput

        classname.text = default_text


    def set_atribute_variance(self, grid, L, R, *args):#, grid, atribute, left, *args):
        
        if((args[1].text).find(': ') < 0):
            #args[1].text =  f'{args[0]}{New.layout(": ")}{args[2]}'
            ######incluir na listagem a ser consuktada
            ######alterar a imagem de exibição


            text = args[0]
            text = New.layout_out(text)

            atribute_list = self.atribute_list_fixed
            fixed = True
            if(args[1].background_color != self.background_color_fixed):
                atribute_list = self.atribute_list_unwished
                fixed = False

            #aux = None
            for i,v in atribute_list.iterrows():
                if(i == text):
                    #aux = v
                    if(fixed):
                        # se é fixo não precisa ter o indesejável
                        
                        if(i in self.atribute_list_unwished.index):
                            if(New.layout_out(args[2]) in self.atribute_list_unwished['valor']):
                                args[1].text =  f'{args[0]}'
                                return
                                # grid.remove_widget(L)
                                # grid.remove_widget(R)
                                # self.atribute_list_unwished=self.atribute_list_unwished.drop([i],axis=0)#remove(v)

                        
                        self.atribute_list_fixed=self.atribute_list_fixed.drop([i],axis=0)#.remove(v)
                    else:
                        # se é indesejável não precisa ter o fixo (mas aqui tem que verificar o valor também)
                        #if(v['valor'] == New.layout_out(args[2])):
                        if(i in self.atribute_list_fixed.index):
                            
                            if(New.layout_out(args[2]) in self.atribute_list_fixed['valor']):
                                grid.remove_widget(L)
                                grid.remove_widget(R)
                                self.atribute_list_unwished=self.atribute_list_unwished.drop([i],axis=0)#remove(v)
                                return
                            else:
                                args[1].text =  f'{args[0]}'
                                return
                            # grid.remove_widget(L)
                            # grid.remove_widget(R)
                            # self.atribute_list_fixed=self.atribute_list_fixed.drop([i],axis=0)#remove(v)

                                
                        self.atribute_list_unwished=self.atribute_list_unwished.drop([i],axis=0)#remove(v)
                    break
            

            args[1].text =  f'{args[0]}{New.layout(": ")}{args[2]}'


            #if(aux is None):
            if(fixed):
                self.atribute_list_fixed=self.atribute_list_fixed.append(pd.DataFrame([New.layout_out(args[2])],index=[text],columns=self.atribute_list_fixed.columns))
            else:
                
                self.atribute_list_unwished=self.atribute_list_unwished.append(pd.DataFrame([New.layout_out(args[2])],index=[text],columns=self.atribute_list_unwished.columns))



            if(self.changing_image is not None):
                self.change_image()
                
            

    @staticmethod
    def layout(text):
        return f'[color=222222][b]{text}[/b][/color]'

    @staticmethod
    def layout_out(text):
        text = text.replace('[color=222222][b]','')
        text = text.replace('[/b][/color]','')
        return text

    # remove a school year from the home menu
    def del_year(self, grid, L, R, *args):
        # remove the two buttons from the GridLayout (year name button and delete button)
        # decrementa a lista de atributos tanto fixos quanto indesejáveis
        text = L.text
        text = New.layout_out(text)
        texts = text.split(': ')

        atribute_list = self.atribute_list_fixed
        fixed = True
        if(L.background_color != self.background_color_fixed):
            atribute_list = self.atribute_list_unwished
            fixed = False

        grid.remove_widget(L)
        grid.remove_widget(R)
        for i,v in atribute_list.iterrows():
            if(i == texts[0]):
                if(fixed):
                    self.atribute_list_fixed=self.atribute_list_fixed.drop([i],axis=0)#.remove(v)
                else:
                    self.atribute_list_unwished=self.atribute_list_unwished.drop([i],axis=0)#remove(v)
                break


        if(self.changing_image is not None):
            self.change_image()
        # if(i is not None):
        #     atribute_list.remove(i)
        #print(atribute_list)
