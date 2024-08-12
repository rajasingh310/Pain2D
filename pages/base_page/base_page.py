from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class BasePage(Screen):
    def __init__(self, **kwargs):
        super(BasePage, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class FirstPage(BasePage):

    def __init__(self, **kwargs):
        super(FirstPage, self).__init__(**kwargs)
        layout = GridLayout(cols=1, rows=2)
        btn_new = Button(text="New")
        btn_import = Button(text="Import")

        btn_new.bind(on_press=self.go_to_menu_page)

        layout.add_widget(btn_new)
        layout.add_widget(btn_import)

        self.add_widget(layout)

    def go_to_menu_page(self, instance):
        self.manager.current = 'menu_page'


class MyApp(App):
    def build(self):
        return FirstPage()


if __name__ == "__main__":
    MyApp().run()