from kivy.uix.screenmanager import Screen
from screens.new import New
from kivy.uix.button import Button
from functools import partial
from model.connect_json import Qvap
from kivy.uix.image import Image
from screens.login import Login
#import kivy.utils as utils

class Results(Screen):
    
    background_color_fixed = [2.4, 2.4, 2.4, 1]

    def build(self):
        super(Results, self)

    def __init__(self):
        super(Results, self).__init__()   

    @staticmethod
    def layout(text):
        return f'[color=222222]{text}[/color]'

    def create(self,grid,scroll_grid,changing_image):

        results = New.get_current_results()
        if(results is None):
            return


        scroll_grid.clear_widgets()

        first = True
        for i,v in results.iterrows():

            my_text = f'{i+1}º'

            #left = SpinnerWidget(values = atribute_variances, text=New.layout(my_text), markup=True, background_color=background, height = 32, size_hint = (1, None))
            
            #aux = left.text
            right = Button(text=Results.layout(my_text), markup=True, background_color=self.background_color_fixed, height = 96, size_hint = (1, None))

            
            #right.text_size = right.size
        
            #right.halign = 'center'
            #right.valign = 'middle'

            right.bind(on_press=partial(self.mark_me, grid, scroll_grid, i, v, right, changing_image))

            icon = Image(source =Qvap.get_image_name([v['material'],v['shape'],v['color'],v['surface'],v['constitution']]),size_hint_x=0.3, size=(60,60))
            #right.add_widget(icon)

            if(first):
                first = False
                right.disabled = True
                Results.select(changing_image,grid,i,v)

                
                    
                # gridLayout = GridLayout()
                # gridLayout.cols = 2
                # gridLayout.minimum_height = 10
                # gridLayout.padding = [0, 0, 0, 0]
                # label_position
                # label_score
                # label_score
                # label_score
                # label_score
                # label_score

                # grid.add_widget(gridLayout)
                


            # the delete button of this year
            
            
            #left.bind(text=partial(self.set_atribute_variance, grid, left, right, aux) )#lambda *args: self.set_atribute_variance(aux, args))

            # equivalent of: on_press = self.del_year(grid, left, right) without NoneType error
            #right.bind(on_press=partial(self.del_year, grid, left, right))

            # add these 2 buttons to the GridLayout
            #grid.add_widget(left)
            scroll_grid.add_widget(icon)
            scroll_grid.add_widget(right)
            right.font_size = right.parent.width * 0.01 + 20


        #print(grid, '***')
    @staticmethod
    def get_weight_color(value,color_green,color_red):
        # color_red = sum_less
        # color_green = sum_most
        # color_blue = 0.0
        fator = 0.9
        if(value > 0):
            fator = 0.95-(value/(color_green))
            return [0.0+fator,(value/(color_green))+fator,0.0+fator,1.0] 
            #print(color_green,(value/(color_green)),(sum_most/value))
        else:
            value = -1*value
            fator = 0.95-(value/(color_red))
            return [(value/(color_red))+fator,0.0+fator,0.0+fator,1.0] 
            #print(color_red,(value/(color_red)),(sum_most/value))
        #print(value,color_red,color_green)
        #return [color_red,color_green,color_blue,1.0]

    @staticmethod
    def select(changing_image,grid,i,v):
        changing_image.source = Qvap.get_image_name([v['material'],v['shape'],v['color'],v['surface'],v['constitution']])
        #print(v)
        atributes_en = Qvap.get_atributes_en()

        sum_most = 0
        sum_less = 0
        
        for c in v.index:
            #print(v[c])
            if(c.find('_weight') >= 0):
                if(v[c] > 0):
                    if(sum_most < v[c]):
                        sum_most = v[c]
                else:
                    if(sum_less > v[c]):
                        sum_less = v[c]
        #print(sum_most,sum_less)
        if(sum_less < 0):
            sum_less = -1 * sum_less

        if(sum_most < 0):
            sum_most = -1 * sum_most

        if(sum_most > sum_less):
            sum_less = sum_most
        else:
            sum_most = sum_less

        for xx in grid.children:
            if(xx.name == 'position'):
                #score = (', QVP = {:{width}.{prec}f}%'.format(v["score"]*100, width=3, prec=2)).replace('.',',')
                xx.text = Results.layout(f'[b]{i+1}º[/b]')
            elif(xx.name == 'score'):
                xx.text = Results.layout(('{:{width}.{prec}f}%'.format(v["score"]*100, width=3, prec=2)).replace('.',','))
            elif(xx.name in atributes_en):
                xx.text = Results.layout(f'{Qvap.translate_atributes_en(xx.name)} = {v[xx.name]}:')
            elif(xx.name.replace('_weight','') in atributes_en):
                #with x.canvas:
                #Color(rgba=self.pencolor)
                #print(x.background)
                #print(Color)
                #x.background_color = Results.get_weight_color(v[x.name],sum_most,sum_less)
                
                xx.background_color = Results.get_weight_color(v[xx.name],sum_most,sum_less)
                #print(x.background_color)
                #x.text = Results.layout('{:{width}.{prec}f}%'.format(v[x.name]*100, width=3, prec=2))

    def mark_me(self, grid, scroll_grid, i, xx, me, changing_image, *args):
        #print(grid.children, me)

        for v in scroll_grid.children:
            if(v != me):
                v.disabled = False
            else:
                v.disabled = True

        Results.select(changing_image,grid,i,xx)
    
    def logoff(self,msg=None):
        if Login.logoff(msg):
            self.manager.transition.direction = 'right'
            self.manager.current = 'login'

    # def on_enter(self):
    #     print(self.children, '++')

    # def on_pre_enter(self):
    #     print(self.children, '+')

    # def on_leave(self):
    #     print(self.children, '--')

    # def on_pre_leave(self):
    #     print(self.children, '-')