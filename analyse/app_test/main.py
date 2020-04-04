#!/usr/bin/env python3
""" from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class MainApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        main_layout.add_widget(self.solution)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            # Clear the solution widget
            self.solution.text = ""
        else:
            if current and (
                self.last_was_operator and button_text in self.operators):
                # Don't add two operators right after each other
                return
            elif current == "" and button_text in self.operators:
                # First character cannot be an operator
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            solution = str(eval(self.solution.text))
            self.solution.text = solution

if __name__ == "__main__":
    app = MainApp()
    app.run() """

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.actionbar import ActionBar

import sys, os
# print( os.environ["PATH"])
# os.environ["PATH"] += ":%s" % os.path.abspath(os.path.join("screens",""))
# print( os.environ["PATH"])
# sys.path.append(os.path.abspath(".."))
# print( os.environ["PATH"])
# from time import sleep
from controler.connect_sqlite import Connection
from screens.splash import Splash
from screens.login import Login
from screens.logup import Logup
from screens.new import New
from screens.profile import Profile
from screens.recents import Recents
from screens.results import Results
from screens.target_audience import TargetAudience
from model.connect_json import Qvap
from widgets.my_spinner import SpinnerWidget

from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


def logoff():
    Login.logoff()
    exit()

atributes=Qvap.get_atributes()#['Material','Cor','Superfície','Forma','Constituição']

class MultiSelectSpinner(Button):
    """Widget allowing to select multiple text options."""

    dropdown = ObjectProperty(None, height = 40)
    """(internal) DropDown used with MultiSelectSpinner."""

    values = ListProperty([])
    # """Values to choose from."""

    selected_values = ListProperty([])
    # """List of values selected by the user."""

    def __init__(self, **kwargs):
        self.bind(dropdown=self.update_dropdown)
        self.bind(values=self.update_dropdown)
        super(MultiSelectSpinner, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_dropdown)

    def toggle_dropdown(self, *args):
        self.values = atributes
        if self.dropdown.parent:
            self.dropdown.dismiss()
        else:
            self.dropdown.open(self)

    def update_dropdown(self, *args):
        if not self.dropdown:
            self.dropdown = DropDown()
        values = self.values
        if values:
            if self.dropdown.children:
                self.dropdown.clear_widgets()
            for value in values:
                b = Factory.MultiSelectOption(text=value)
                b.bind(state=self.select_value)
                self.dropdown.add_widget(b)

    def select_value(self, instance, value):
        for v in self.selected_values:
            self.selected_values.remove(v)
        self.selected_values.append(instance.text)

    def on_selected_values(self, instance, value):
        if value:
            self.text = ', '.join(value)
        else:
            self.text = ''

    def on_selected_values(self, instance, value):
        if value:
            self.text = ', '.join(value)
        else:
            self.text = ''
            






# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""


#: import utils kivy.utils

<BackgroundColor@Widget>
    background_color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: self.size
            pos: self.pos    
<BackgroundLabel@Label+BackgroundColor>
    background_color: 0, 0, 0, 0

<Splash>:
    name: 'splash'
    BoxLayout:
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#bdbfc1')
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        pos_hint: {'top': 1}
        height: 44
        Image:
            size: 24, 24
            source: 'images/splash.gif'

<Login>:
    name: 'login'
    FloatLayout:
        id: 'layout'
        orientation: 'vertical'
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#bdbfc1')
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Image:
            size: 200, 200
            size_hint_y: None
            pos: 0, self.parent.height - 230
            source: 'images/splash.gif'

        ActionBar:
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    app_icon: ''
                    title: 'Login'
                    with_previous: False
                ActionOverflow:
                ActionButton:
                    text: 'Sair'
                    on_press: 
                        exit()
        GridLayout:
            cols: 1
            orientation: 'vertical'
            size_hint_y: None
            pos: 0, self.parent.height - 315
            row_force_default: True 
            row_default_height: self.parent.height

        
            ScrollView:


                size_hint:(1, .8)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}

                pos: 0, self.parent.height - 315

                do_scroll_x: False
                #height: self.parent.height

                GridLayout:
                    cols: 1
                    orientation: 'vertical'
                    size_hint: (1, None)
                    pos: 0, self.parent.height - 315
                    #row_force_default: True 
                    row_default_height: 110
                    height: self.minimum_height

                    GridLayout:
                        cols: 2
                        id: main_grid
                        name: 'main_grid'
                        orientation: 'vertical'
                        row_force_default: True 
                        row_default_height: 45
                        spacing: 5
                        Label:  
                            markup: True
                            
                            text: "[color=222222][b]Login (e-mail)[/b][/color]"   

                            font_size: 18


                            text_size: self.size
                            halign: 'right'
                            valign: 'middle'

                        TextInput:
                            id: login
                            multiline: False
                            halign: 'left'                            
                            valign: 'middle'
                            font_size: 20
                        
                        Label:  
                            markup: True
                            
                            text: "[color=222222][b]Senha[/b][/color]"   

                            text_size: self.size
                            halign: 'right'
                            valign: 'middle'
                            font_size: 18
                        TextInput:
                            id: password
                            password: True
                            multiline: False
                            halign: 'left'                         
                            valign: 'middle'
                            font_size: 20

                    GridLayout:
                        cols: 1
                        id: main_grid_2
                        name: 'main_grid_2'
                        orientation: 'vertical'
                        row_force_default: True 
                        row_default_height: 45
                        
                        Button:
                            text: 'entrar'
                            on_press: 
                                root.check_login(login,password,msg)
                        Button:
                            text: 'ainda não tenho cadastro'
                            on_press: 
                                root.manager.transition.direction = 'left'
                                root.manager.current = 'logup'
        
        BackgroundLabel:
            id: msg
            size_hint_y: None
            pos: 0, 0
            markup: True
            text: "[color=222222][b][/b][/color]"
            height: 20
            background_color: 1, 1, 1, 1
<Recents>:
    name: 'recents'
    on_enter: root.clear_message(msg)
    FloatLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#bdbfc1')
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Image:
            size: 200, 200
            size_hint_y: None
            pos: 0, self.parent.height - 230
            source: 'images/splash.gif'
        ActionBar:
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    app_icon: ''
                    title: 'Recentes'
                    with_previous: False
                ActionOverflow:
                ActionButton:
                    text: 'Nova consulta'
                    on_press: 
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'new'
                ActionGroup:
                    text: 'Mais'
                    ActionButton:
                        text: 'Atualizar'
                        # text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        on_press: 
                            root.manager.transition.direction = 'left'
                            root.manager.current = 'profile'
                    ActionButton:
                        text: 'Logoff'
                        # text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        on_press:
                            root.logoff(msg)
                    ActionButton:
                        text: 'Sair'
                        on_press: 
                            exit()
        BackgroundLabel:
            id: msg
            size_hint_y: None
            pos: 0, 0
            markup: True
            text: "[color=222222][b][/b][/color]"
            height: 20
            background_color: 1, 1, 1, 1
<Profile>:
    name: 'profile'
    on_enter: root.set_all(main_grid,msg)
    FloatLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#bdbfc1')
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Image:
            size: 200, 200
            size_hint_y: None
            pos: 0, self.parent.height - 230
            source: 'images/splash.gif'

        ActionBar:
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    app_icon: ''
                    title: 'Atualizar'
                    with_previous: False
                ActionOverflow:
                ActionButton:
                    text: 'Consultar'
                    on_press: 
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'new'
                ActionGroup:
                    text: 'Mais'
                    ActionButton:
                        text: 'Recentes'
                        # text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        on_press: 
                            root.manager.transition.direction = 'left'
                            root.manager.current = 'recents'
                    ActionButton:
                        text: 'Logoff'
                        # text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        on_press: 
                            root.logoff(msg)
                    ActionButton:
                        text: 'Sair'
                        on_press: 
                            exit()
        GridLayout:
            cols: 1
            orientation: 'vertical'
            size_hint_y: None
            pos: 0, self.parent.height - 315
            row_force_default: True 
            row_default_height: self.parent.height

        
            ScrollView:


                size_hint:(1, .8)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}

                pos: 0, self.parent.height - 315

                do_scroll_x: False
                #height: self.parent.height

                GridLayout:
                    cols: 1
                    orientation: 'vertical'
                    size_hint: (1, None)
                    pos: 0, self.parent.height - 315
                    #row_force_default: True 
                    row_default_height: 55
                    height: self.minimum_height

                    GridLayout:
                        cols: 2
                        id: main_grid
                        name: 'main_grid'
                        orientation: 'vertical'
                        row_force_default: True 
                        row_default_height: 45
                        
                        Label:  
                            markup: True
                            
                            text: "[color=222222][b]E-mail[/b][/color]"   

                            font_size: 18


                        TextInput:
                            id: email
                            name: 'email'
                            readonly: True
                            disabled: True
                            multiline: False
                            halign: 'left'
                            valign: 'middle'
                            font_size: 20
                    Button:
                        text: 'Atualizar senha'
                    Button:
                        text: 'Configurações'
                    Button:
                        text: 'Ok'
                        on_press: 
                            root.manager.transition.direction = 'right'
                            root.manager.current = 'recents'

        BackgroundLabel:
            id: msg
            size_hint_y: None
            pos: 0, 0
            markup: True
            text: "[color=222222][b][/b][/color]"
            height: 20
            background_color: 1, 1, 1, 1
                
<MultiSelectOption@ToggleButton>:
    size_hint: 1, None
    height: '32dp'


<New>:
    name: 'new'
    on_enter: root.clear_message(msg)
    
    FloatLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.95, 0.951, 0.95, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        ActionBar:
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    app_icon: ''
                    title: 'Nova consulta'
                    with_previous: False
                ActionOverflow:
                ActionButton:
                    text: 'Recentes'
                    on_press: 
                        root.manager.transition.direction = 'right'
                        root.manager.current = 'recents'
                ActionGroup:
                    text: 'Mais'
                    ActionButton:
                        text: 'Logoff'
                        # text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        on_press: 
                            root.logoff(msg)
                    ActionButton:
                        text: 'Sair'
                        # text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        on_press: 
                            exit()

                
                # ActionButton:
                #     text: 'Público'
                #     on_press: 
                #         root.manager.transition.direction = 'left'
                #         root.manager.current = 'profile'

        GridLayout:
            cols: 1

            orientation: 'vertical'
            row_force_default: True 
            row_default_height: self.parent.height * 0.4
            #pos: 0, self.parent.height * 0.09 * -1
            pos: 0, -55
            Image:
                id: changing_image
                size: 24, self.parent.height
                source: 'images/png/XG.gif'
                size_hint: (1, 1)
            
        GridLayout:
            cols: 2
            orientation: 'vertical'
            row_force_default: True 
            row_default_height: self.parent.height * 0.3
            size: self.parent.width, self.parent.height
            canvas.before:
                Color:
                    rgba: 0.95, 0.951, 0.95, 1
                Rectangle:
                    # self here refers to the widget i.e FloatLayout
                    pos: self.pos
                    size: self.size


            pos: 0, self.parent.height * 0.53 * -1
            padding: 10
            spacing: 0
            GridLayout:
                cols: 1
                orientation: 'vertical'
                row_force_default: True 
                row_default_height: 30
                spacing: 10
                
                Label:
                    #text: 'Atributos'    
                    markup: True
                    
                    text: "[color=222222][b]Atributos[/b][/color]"   

                    font_size: self.parent.width * 0.01 + 14
                    
                GridLayout:
                    id: layout
                    cols: 1
                    orientation: 'vertical'
                    row_force_default: True 
                    row_default_height: 30
                    padding: 0
                    spacing: 2
                    
                    BoxLayout:

                        padding: 5
                        spacing: 5
                        size: (42, 42)
                        size_hint: (1, None)

                        SpinnerWidget: 
                            # Assigning id  
                            id: fixo 
                    
                            # Callback  
                            on_text: root.spinner_clicked(changing_image,home_scroll_grid, fixo, '[color=222222][b]Fixos[/b][/color]') 
                    
                            markup: True
                            # initially text on spinner 
                            text: "[color=222222][b]Fixos[/b][/color]"

                            background_color: [2.8, 2.8, 2.8, 1]

                            # total values on spinner 
                            values: root.get_atributes()
                    
                            # declaring size of the spinner 
                            # and the position of it 
                            size_hint: 1, None
                            size: self.parent.width, 32
                            pos_hint:{'center_x':.5, 'top': 1} 
                            
                            text_size: self.size
                            halign: 'center'
                            valign: 'middle'


    

                    BoxLayout:

                        padding: 5
                        spacing: 5
                        size: (42, 42)
                        size_hint: (1, None)

                        SpinnerWidget: 
                            # Assigning id  
                            id: indesejavel 
                    
                            # Callback  
                            on_text: root.spinner_clicked(changing_image, home_scroll_grid, indesejavel, '[color=222222][b]Indesejáveis[/b][/color]') 
                    
                            markup: True
                            # initially text on spinner 
                            text: "[color=222222][b]Indesejáveis[/b][/color]"
                            # initially text on spinner 
                            # text: "Indesejáveis"

                            background_color: [7, 2, 2, 1]
                            # background_color: [1, 0.3, 0.3, 1]
                    
                            # total values on spinner 
                            values: root.get_atributes()
                    
                            # declaring size of the spinner 
                            # and the position of it 
                            size_hint: 1, None
                            size: self.parent.width, 32
                            pos_hint:{'center_x':.5, 'top': 1} 
                            
                            text_size: self.size
                            halign: 'center'
                            valign: 'middle'

                

                
                 
                    
                    
            

            ScrollView:


                size_hint:(1, .8)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                do_scroll_x: False
                #height: self.parent.height
                GridLayout:
                    id: home_scroll_grid
                    cols: 2
                    padding: 5
                    spacing: 5
                    height: self.minimum_height
                    size_hint: (1, None)
        GridLayout:
            cols: 1
            orientation: 'vertical'
            row_force_default: True 
            row_default_height: self.parent.height * 0.1
            # pos: 100, self.parent.height - self.height - 100
            pos: 0, self.parent.height * 0.9 * -1 + 20
            spacing: 0
            Button:
                text: 'Consultar'
                font_size: self.parent.width * 0.01 + 12
                on_press: 
                    root.query(msg)
        BackgroundLabel:
            id: msg
            size_hint_y: None
            pos: 0, 0
            markup: True
            text: "[color=222222][b][/b][/color]"
            height: 20
            background_color: 1, 1, 1, 1


<Results>:
    name: 'results'
    on_pre_enter: root.create(home_grid,home_scroll_grid_2,changing_image_2)

    FloatLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.95, 0.95, 0.95, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        ActionBar:
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    app_icon: ''
                    title: 'Resultados'
                    with_previous: False
                ActionOverflow:
                ActionButton:
                    text: 'Recentes'
                    on_press: 
                        root.manager.transition.direction = 'right'
                        root.manager.current = 'recents'
                ActionGroup:
                    text: 'Mais'
                    ActionButton:
                        text: 'Logoff'
                        # text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        on_press: 
                            root.logoff(msg)
                    ActionButton:
                        text: 'Sair'
                        # text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        on_press: 
                            exit()

                
                # ActionButton:
                #     text: 'Público'
                #     on_press: 
                #         root.manager.transition.direction = 'left'
                #         root.manager.current = 'profile'

        GridLayout:
            cols: 1
            orientation: 'vertical'
            row_force_default: True 
            row_default_height: 230
            pos: 0, self.parent.height * 0.09 * -1
            spacing: 10
            GridLayout:
                cols: 2
                orientation: 'vertical'
                row_force_default: True 
                row_default_height: 230
                padding: 10
                spacing: 10
                Image:
                    id: changing_image_2
                    size: 17, 17
                    source: 'images/png/XG.png'
                GridLayout:
                    cols: 2
                    id: home_grid
                    
                    spacing: 2
                    
                    Label:    
                        id: position
                        name: 'position'
                        markup: True
                        text: "[color=111111][b]1º[/b][/color]"   
                        font_size: self.parent.width * 0.01 + 20
                        
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                    Label:    
                        name: ''
                        markup: True
                        text: "[color=222222][b] [/b][/color]"   
                        font_size: self.parent.width * 0.01 + 14
                        size_hint_x: 0.3
                        text_size: self.size
                        halign: 'right'
                        valign: 'middle'
                    Label:    
                        name: ''
                        markup: True
                        text: "[color=222222][b]QVP:[/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        
                        text_size: self.size
                        halign: 'left'
                        valign: 'middle'
                    Label:    
                        id: score
                        name: 'score'
                        markup: True
                        text: "[color=222222][b][/b][/color]"   
                        font_size: self.parent.width * 0.01 + 10
                        size_hint_x: 0.3
                        text_size: self.size
                        halign: 'right'
                        valign: 'middle'
                        #background_color: 1, 0.951, 0.95, 1

                    Label:    
                        id: material
                        name: 'material'
                        markup: True
                        text: "[color=222222][b]Material = Metal:[/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        
                        text_size: self.size
                        halign: 'left'
                        valign: 'middle'
                    BackgroundLabel:    
                        id: material_weight
                        name: 'material_weight'
                        markup: True
                        text: "[color=222222][b] [/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        size_hint_x: 0.3
                        text_size: self.size
                        halign: 'right'
                        valign: 'middle'
                        background_color: 1, 0.951, 0.95, 1

                    Label:    
                        id: color
                        name: 'color'
                        markup: True
                        text: "[color=222222][b]Cor = Intensa:[/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        
                        text_size: self.size
                        halign: 'left'
                        valign: 'middle'
                    BackgroundLabel:    
                        id: color_weight
                        name: 'color_weight'
                        markup: True
                        text: "[color=222222][b] [/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        size_hint_x: 0.3
                        text_size: self.size
                        halign: 'right'
                        valign: 'middle'
                        background_color: 1, 0.951, 0.95, 1
                    Label:    
                        id: shape
                        name: 'shape'
                        markup: True
                        text: "[color=222222][b]Forma = Geométrica[/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        
                        text_size: self.size
                        halign: 'left'
                        valign: 'middle'
                    BackgroundLabel:    
                        id: shape_weight
                        name: 'shape_weight'
                        markup: True
                        text: "[color=222222][b] [/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        size_hint_x: 0.3
                        text_size: self.size
                        halign: 'right'
                        valign: 'middle'
                        background_color: 1, 0.951, 0.95, 1
                    Label:    
                        id: surface
                        name: 'surface'
                        markup: True
                        text: "[color=222222][b]Superfície = Fosca[/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        
                        text_size: self.size
                        halign: 'left'
                        valign: 'middle'
                    BackgroundLabel:    
                        id: surface_weight
                        name: 'surface_weight'
                        markup: True
                        text: "[color=222222][b] [/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        size_hint_x: 0.3
                        text_size: self.size
                        halign: 'right'
                        valign: 'middle'
                        background_color: 1, 0.951, 0.95, 1
                    Label:    
                        id: constitution
                        name: 'constitution'
                        markup: True
                        text: "[color=222222][b]Constituição = Compexidade[/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        
                        text_size: self.size
                        halign: 'left'
                        valign: 'middle'
                        background_color: 1, 0.951, 0.95, 1
                    BackgroundLabel:    
                        id: constitution_weight
                        name: 'constitution_weight'
                        markup: True
                        text: "[color=222222][b] [/b][/color]"   
                        font_size: self.parent.width * 0.01 + 12
                        size_hint_x: 0.3
                        text_size: self.size
                        halign: 'right'
                        valign: 'middle'
                        background_color: 1, 0.951, 0.95, 1
                
        

            ScrollView:

                size_hint:(1, .8)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                do_scroll_x: False
                auto_width: True
                GridLayout:
                    id: home_scroll_grid_2
                    cols: 2
                    
                    padding: 0
                    spacing: 0
                    height: self.minimum_height
                    size_hint: (1, None)


        GridLayout:
            cols: 2
            orientation: 'vertical'
            row_force_default: True 
            row_default_height: self.parent.height * 0.1
            # pos: 100, self.parent.height - self.height - 100
            pos: 0, self.parent.height * 0.9 * -1 + 20
            spacing: 0
            Button:
                text: 'Nova consulta'
                font_size: self.parent.width * 0.01 + 12
                on_press: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'new'
            Button:
                text: 'Salvar'
                font_size: self.parent.width * 0.01 + 12
                background_color: 1.2, 2, 1.2, 1
                on_press: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'recents'
        GridLayout:
            cols: 1
            orientation: 'vertical'
            size_hint_y: None
            row_force_default: True 
            row_default_height: 20
            pos: 0, -80 #self.parent.height * 0.9 * -1
            
            padding: 0
            spacing: 0

            BackgroundLabel:
                id: msg
                size_hint_y: None
                pos: 0, 0
                markup: True
                text: "[color=222222][b][/b][/color]"
                height: 20
                background_color: 1, 1, 1, 1

















<TargetAudience>:
    name: 'target_audience'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Público alvo'
        Button:
            text: 'Voltar'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'new'
        Button:
            text: 'Consultas recentes'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'recents'
        Button:
            text: 'sair'
            on_press: 
                exit()

<Logup>:
    name: 'logup'
    
    FloatLayout:
        id: 'layout'
        orientation: 'vertical'
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#bdbfc1')
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Image:
            size: 200, 200
            size_hint_y: None
            pos: 0, self.parent.height - 230
            source: 'images/splash.gif'

        ActionBar:
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    app_icon: ''
                    title: 'Login'
                    with_previous: False
                ActionOverflow:
                ActionButton:
                    text: 'Sair'
                    on_press: 
                        exit()
        GridLayout:
            cols: 1
            orientation: 'vertical'
            size_hint_y: None
            pos: 0, self.parent.height - 315
            row_force_default: True 
            row_default_height: self.parent.height

        
            ScrollView:


                size_hint:(1, .8)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}

                pos: 0, self.parent.height - 315

                do_scroll_x: False
                #height: self.parent.height

                GridLayout:
                    cols: 1
                    orientation: 'vertical'
                    size_hint: (1, None)
                    pos: 0, self.parent.height - 315
                    #row_force_default: True 
                    row_default_height: 165
                    height: self.minimum_height

                    GridLayout:
                        cols: 2
                        id: main_grid
                        name: 'main_grid'
                        orientation: 'vertical'
                        row_force_default: True 
                        row_default_height: 45
                        spacing: 5
                        
                        Label:  
                            markup: True
                            
                            text: "[color=222222][b]E-mail[/b][/color]"   

                            text_size: self.size
                            halign: 'right'
                            valign: 'middle'
                            font_size: 18



                        TextInput:
                            id: email
                            multiline: False
                            halign: 'left'                         
                            valign: 'middle'
                            font_size: 20



                        
                        Label:  
                            markup: True
                            
                            text: "[color=222222][b]Senha[/b][/color]"   

                            text_size: self.size
                            halign: 'right'
                            valign: 'middle'
                            
                            font_size: 18
                        TextInput:
                            id: password
                            password: True
                            multiline: False
                            halign: 'left'                         
                            valign: 'middle'
                            font_size: 20



                        
                        Label:  
                            markup: True
                            
                            text: "[color=222222][b]Confirmar enha[/b][/color]"   

                            text_size: self.size
                            halign: 'right'
                            valign: 'middle'
                            font_size: 18
                        TextInput:
                            id: confirm_password
                            password: True
                            multiline: False
                            halign: 'left'                         
                            valign: 'middle'
                            font_size: 20


                    GridLayout:
                        cols: 1
                        id: main_grid_2
                        name: 'main_grid_2'
                        orientation: 'vertical'
                        row_force_default: True 
                        row_default_height: 45
                        
                        Button:
                            text: 'cadastrar'
                            on_press:
                                root.record(email,password,confirm_password,msg)
                        Button:
                            text: 'voltar ao login'
                            on_press: 
                                root.manager.transition.direction = 'right'
                                root.manager.current = 'login'
        
        BackgroundLabel:
            id: msg
            size_hint_y: None
            pos: 0, 0
            markup: True
            text: "[color=222222][b]fgffdgh[/b][/color]"
            height: 20
            background_color: 1, 1, 1, 1
""")

# Declare both screens
# class MenuScreen(Screen):
#     pass

# class SettingsScreen(Screen):
#     pass

# Create the screen manager
sm = ScreenManager()
lg = Login()
sm.add_widget(Splash())
sm.add_widget(lg)
sm.add_widget(Logup())
sm.add_widget(Recents())
sm.add_widget(New())
sm.add_widget(Results())
sm.add_widget(TargetAudience())
sm.add_widget(Profile.get_instance())



class TestApp(App):

    def build(self):
        Clock.schedule_once(self.screen_switch_one, 3)
        return sm

    def screen_switch_one(a,b):
        #check login previo
        if(Login.just_logged(Login.get_connection())):
            sm.current = 'recents'
        else:
            sm.current = 'login'

    @staticmethod
    def exit():
        Login.close_connection()
        exit()

   

# class TestApp(App):

#     def build(self):
#         return sm

if __name__ == '__main__':
    TestApp().run()