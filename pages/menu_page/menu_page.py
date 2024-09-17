from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from ..base_page.base_page import BasePage


class MenuPage(BasePage):
    def __init__(self, **kwargs):
        super(MenuPage, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation="vertical")

        top_nested_layout = BoxLayout(orientation="vertical")

        #btn1 = Button(text="Patient Info")
        #btn2 = Button(text="Questionnaire Info")
        #btn3 = Button(text="Laboratory Info")
        btn4 = Button(text="SeePain Info")

        #btn1.bind(on_press=self.go_to_patient_page)
        #btn2.bind(on_press=self.go_to_questionnaire_page)
        #btn3.bind(on_press=self.go_to_laboratory_page)
        btn4.bind(on_press=self.go_to_seepain_page)

        #top_nested_layout.add_widget(btn1)
        #top_nested_layout.add_widget(btn2)
        #top_nested_layout.add_widget(btn3)
        top_nested_layout.add_widget(btn4)

        bottom_nested_layout = BoxLayout(orientation="vertical")

        #btn5 = Button(text="Submit", background_color=(0, 1, 0, 1))
        btn6 = Button(text="Back", background_color=(1, 0, 0, 1))

        btn6.bind(on_press=self.go_back)

        #bottom_nested_layout.add_widget(btn5)
        bottom_nested_layout.add_widget(btn6)

        # Set the size_hint for the nested layouts before adding them
        top_nested_layout.size_hint = (1, 0.9)
        bottom_nested_layout.size_hint = (1, 0.1)

        # Add both nested layouts to the main layout
        main_layout.add_widget(top_nested_layout)
        main_layout.add_widget(bottom_nested_layout)

        self.add_widget(main_layout)

    def go_to_patient_page(self, instance):
        self.manager.current = 'patient_page'

    def go_to_questionnaire_page(self, instance):
        self.manager.current = 'questionnaire_page'

    def go_to_laboratory_page(self, instance):
        self.manager.current = 'laboratory_page'

    def go_to_seepain_page(self, instance):
        self.manager.current = 'seepain_page'

    def go_back(self, instance):
        self.manager.current = 'first_page'


class MyApp(App):
    def build(self):
        return MenuPage()


if __name__ == "__main__":
    MyApp().run()