from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
class PatientInfo(GridLayout):

    def __init__(self, **kwargs):
        super(PatientInfo, self).__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size)

        Window.bind(size=self.update_rect)

        self.cols = 1

        self.top_grid = GridLayout()
        self.top_grid.cols = 2

        self.top_grid.add_widget(Label(text="1. Id:", font_size="8mm",  color=(0, 0, 0, 1)))
        self.top_grid.add_widget(TextInput(multiline=False, font_size="8mm"))


        patient_info_list = ["First name: ", "Last name: ", "Date of birth: ", "Gender: ", "Address: ", "Phone number: ", "Email address: "]

        i = 2
        for p in patient_info_list:
            self.top_grid.add_widget(
                Label(text=f"{i}. {p} ", font_size="8mm", color=(0, 0, 0, 1)))
            self.top_grid.add_widget(TextInput(multiline=False, font_size="8mm"))
            i += 1

        self.top_grid.add_widget(Button(text="Submit", font_size="8mm", color=(0, 0, 0, 1), background_color=(0, 1, 0, 1)))
        self.top_grid.add_widget(Button(text="Back", font_size="8mm", color=(0, 0, 0, 1), background_color=(1, 0, 0, 1)))


    def update_rect(self, *args):
        self.rect.size = Window.size


class PatientInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(PatientInfoScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size)

        Window.bind(size=self.update_rect)

        self.add_widget(PatientInfo().top_grid)

    def update_rect(self, *args):
        self.rect.size = Window.size



class X(App):
    def build(self):
        return PatientInfo()

if __name__ == "__main__":
    X().run()



