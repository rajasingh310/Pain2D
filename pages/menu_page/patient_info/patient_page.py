from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from ...base_page.base_page import BasePage


class PatientPage(BasePage):

    def __init__(self, **kwargs):
        super(PatientPage, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation="vertical")

        # Top nested layout with 2 columns and 3 rows
        top_nested_layout = GridLayout(cols=2, rows=8)

        patient_info_list = ["Id: ", "First name: ", "Last name: ", "Date of birth: ", "Gender: ", "Address: ",
                             "Phone number: ", "Email address: "]

        i = 1
        for p in patient_info_list:
            top_nested_layout.add_widget(
                Label(text=f"{i}. {p} ", color=(0, 0, 0, 1)))
            top_nested_layout.add_widget(TextInput(multiline=False))
            i += 1

        # Bottom nested layout with 1 column and 2 rows
        bottom_nested_layout = GridLayout(cols=1, rows=2)

        btn_submit = Button(text="Submit", background_color=(0, 1, 0, 1))
        btn_back = Button(text="Back", background_color=(1, 0, 0, 1))

        btn_back.bind(on_press=self.go_back)

        bottom_nested_layout.add_widget(btn_submit)
        bottom_nested_layout.add_widget(btn_back)

        # Set the size_hint for the nested layouts before adding them
        top_nested_layout.size_hint = (1, 0.9)
        bottom_nested_layout.size_hint = (1, 0.1)

        # Add both nested layouts to the main layout
        main_layout.add_widget(top_nested_layout)
        main_layout.add_widget(bottom_nested_layout)

        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.current = 'menu_page'


class MyApp(App):
    def build(self):
        return PatientPage()


if __name__ == "__main__":
    MyApp().run()



