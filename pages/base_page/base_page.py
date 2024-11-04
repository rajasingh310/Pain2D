from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.core.image import Image as CoreImage


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
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # Load the image
        self.bg_image = CoreImage('pages/base_page/logo.png').texture

        # Create an Image widget and set its texture, occupying top 20% of the screen
        image_widget = KivyImage()
        image_widget.texture = self.bg_image
        image_widget.size_hint_y = 0.3  # 20% of the screen height
        layout.add_widget(image_widget)

        # Add a label for the heading "SeePain", occupying the remaining space
        label_heading = Label(text="[b]SeePain[/b]", markup=True, font_size='32sp', halign="center", size_hint_y=0.2, color=(0, 0.5, 0.5, 1))
        layout.add_widget(label_heading)

        # Add a label for the German description, occupying the remaining space
        label_description = Label(text="Willkommen bei der SeePain-App. \nHier können Sie Ihren Schmerz auf einem Körper visualisieren.", font_size='18sp', halign="center", valign="middle", size_hint_y=0.4, color=(0, 0, 0, 1))
        layout.add_widget(label_description)

        # Add the ENTER button, occupying bottom 20% of the screen
        btn_new = Button(text="Start", size_hint_y=0.15, background_color = (0, 1, 0, 1))
        btn_new.bind(on_press=self.go_to_menu_page)

        layout.add_widget(btn_new)

        self.add_widget(layout)

    def go_to_menu_page(self, instance):
        self.manager.current = 'menu_page'


class MyApp(App):
    def build(self):
        return FirstPage()


if __name__ == "__main__":
    MyApp().run()
