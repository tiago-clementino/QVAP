from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown


class SpinnerOptions(SpinnerOption):

    def __init__(self, **kwargs):
        super(SpinnerOptions, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0.9, 0.9, 0.9, 1]#[0.5, 0.5, 0.55, 1]    # blue colour
        self.height = 32
        self.markup = True
        self.text = SpinnerOptions.format(self.text)
        
    @staticmethod
    def format(text):
        return f'[color=222222][b]{text}[/b][/color]'
        
    @staticmethod
    def format_out(text):
        text = text.replace('[color=222222][b]','')
        text = text.replace('[/b][/color]','')
        return text


class SpinnerDropdown(DropDown):

    def __init__(self, **kwargs):
        super(SpinnerDropdown, self).__init__(**kwargs)
        
        self.auto_width = True
        #self.width = 150


class SpinnerWidget(Spinner):

    def __init__(self, **kwargs):
        super(SpinnerWidget, self).__init__(**kwargs)

        self.dropdown_cls = SpinnerDropdown
        
        self.option_cls = SpinnerOptions

        self.auto_width = True
        
        self.halign = 'center'
        self.valign = 'middle'


        