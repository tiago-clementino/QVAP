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

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""

<Splash>:
    name: 'splash'
    BoxLayout:
        pos_hint: {'top': 1}
        height: 44
        Image:
            size: 24, 24
            source: 'images/splash.png'

<Login>:
    name: 'login'
    BoxLayout:
        id: 'layout'
        orientation: 'vertical'
        Label:
            text: 'Entre com o seu login'
        TextInput:
            id: login
            multiline: False
            halign: 'left'
            font_size: 55
        TextInput:
            id: password
            password: True
            multiline: False
            halign: 'left'
            font_size: 55
        Button:
            text: 'entrar'
            on_press: 
                root.check_login(login,password,msg)
        Button:
            text: 'ainda não tenho cadastro'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'logup'
        Button:
            text: 'sair'
            on_press: 
                exit()
        Label:
            id: msg
            text: ''
<Recents>:
    name: 'recents'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Consultas recentes'
        Button:
            text: 'Nova consulta'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'new'
        Button:
            text: 'Atualizar cadastro'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'profile'
        Button:
            text: 'sair'
            on_press: 
                exit()
<Profile>:
    name: 'profile'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Atualizações'
        TextInput:
            id: email
            readonly: True
            multiline: False
            halign: 'left'
            font_size: 55
        Button:
            text: 'Atualizar senha'
        Button:
            text: 'Configurações'
        Button:
            text: 'Voltar'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'recents'
        Button:
            text: 'sair'
            on_press: 
                exit()
<New>:
    name: 'new'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Nova consulta'
        Button:
            text: 'Consultar'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'results'
        Button:
            text: 'Definir público alvo'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'results'
        Button:
            text: 'Voltar'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'recents'
        Button:
            text: 'sair'
            on_press: 
                exit()
<Results>:
    name: 'results'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Resultados'
        Button:
            text: 'Nova consulta'
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
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Cadastro'
        TextInput:
            id: email
            multiline: False
            halign: 'left'
            font_size: 55
        TextInput:
            id: password
            password: True
            multiline: False
            halign: 'left'
            font_size: 55
        TextInput:
            id: confirm_password
            password: True
            multiline: False
            halign: 'left'
            font_size: 55
        Button:
            text: 'cadastrar'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'recents'
        Button:
            text: 'voltar ao login'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'login'
        Button:
            text: 'sair'
            on_press: 
                exit()
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
sm.add_widget(Profile())

class TestApp(App):

    def build(self):
        Clock.schedule_once(self.screen_switch_one, 3)
        return sm

    def screen_switch_one(a,b):
        #check login previo
        if(Login.just_logged(lg.get_connection())):
            sm.current = 'recents'
        else:
            sm.current = 'login'

   

# class TestApp(App):

#     def build(self):
#         return sm

if __name__ == '__main__':
    TestApp().run()