from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from ...base_page.base_page import BasePage


class LaboratoryPage(BasePage):
    def __init__(self, **kwargs):
        super(LaboratoryPage, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation="vertical")

        top_nested_layout = BoxLayout(orientation="vertical")

        label = Label(text="Update coming soon!", color=(0, 0, 0, 1))
        top_nested_layout.add_widget(label)

        bottom_nested_layout = BoxLayout(orientation="vertical")

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
        return LaboratoryPage()


if __name__ == "__main__":
    MyApp().run()