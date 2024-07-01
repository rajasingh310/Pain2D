from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager, Screen


class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (1, 0, 0, 1)  # Default to red
        self.line_width = 2

        # Load the image
        with self.canvas:
            self.bg = CoreImage('pain2d_info/human_sketch_2.png').texture
            self.rect = Rectangle(texture=self.bg, pos=self.pos, size=self.size)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.color)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]
            return True
        return super().on_touch_move(touch)

    def clear_canvas(self):
        self.canvas.clear()
        with self.canvas:
            self.rect = Rectangle(texture=self.bg, pos=self.pos, size=self.size)

    def save_canvas(self):
        self.export_to_png("painted_image.png")

class Pain2D_draw(Screen):
    def __init__(self, **kwargs):
        super(Pain2D_draw, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.paint_widget = PaintWidget()
        layout.add_widget(self.paint_widget)

        button_layout = BoxLayout(size_hint=(1, 0.1))

        color_picker_button = Button(text='Choose Color')
        color_picker_button.bind(on_release=self.open_color_picker)
        button_layout.add_widget(color_picker_button)

        clear_button = Button(text='Clear')
        clear_button.bind(on_release=self.clear_canvas)
        button_layout.add_widget(clear_button)

        save_button = Button(text='Save')
        save_button.bind(on_release=self.save_canvas)
        button_layout.add_widget(save_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)

    def open_color_picker(self, instance):
        color_picker = ColorPicker()
        popup = Popup(title='Pick a Color', content=color_picker, size_hint=(0.8, 0.8))
        color_picker.bind(color=self.on_color)
        popup.open()

    def on_color(self, instance, value):
        self.paint_widget.color = value

    def clear_canvas(self, instance):
        self.paint_widget.clear_canvas()

    def save_canvas(self, instance):
        self.paint_widget.save_canvas()

