from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from ...base_page.base_page import BasePage

from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.image import Image as CoreImage


class SeePainPage(BasePage):
    def __init__(self, **kwargs):
        super(SeePainPage, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation="vertical")

        # Top nested layout
        top_nested_layout = BoxLayout(orientation="vertical")

        self.paint_widget = PaintWidget()
        top_nested_layout.add_widget(self.paint_widget)

        # middle nested layout
        middle_nested_layout = BoxLayout(orientation="horizontal")

        color_picker_button = Button(text='Choose Color')
        color_picker_button.bind(on_release=self.open_color_picker)
        middle_nested_layout.add_widget(color_picker_button)

        clear_button = Button(text='Clear')
        clear_button.bind(on_release=self.clear_canvas)
        middle_nested_layout.add_widget(clear_button)

        save_button = Button(text='Save')
        save_button.bind(on_release=self.save_canvas)
        middle_nested_layout.add_widget(save_button)

        # Bottom nested layout with 1 column and 2 rows
        bottom_nested_layout = GridLayout(cols=1, rows=2)

        btn_submit = Button(text="Submit", background_color=(0, 1, 0, 1))
        btn_back = Button(text="Back", background_color=(1, 0, 0, 1))

        btn_back.bind(on_press=self.go_back)

        bottom_nested_layout.add_widget(btn_submit)
        bottom_nested_layout.add_widget(btn_back)

        # Set the size_hint for the nested layouts before adding them
        top_nested_layout.size_hint = (1, 0.8)
        middle_nested_layout.size_hint = (1, 0.1)
        bottom_nested_layout.size_hint = (1, 0.1)

        # Add nested layouts to the main layout
        main_layout.add_widget(top_nested_layout)
        main_layout.add_widget(middle_nested_layout)
        main_layout.add_widget(bottom_nested_layout)

        self.add_widget(main_layout)

    def open_color_picker(self, instance):
        color_grid = BoxLayout(orientation="vertical", spacing=10, size_hint=(1, 1))
        colors = [
            (1, 0, 0, 1), (1, 0.2, 0, 1), (1, 0.3, 0, 1), (1, 0.4, 0, 1), (1, 0.5, 0, 1),
            (1, 0.6, 0, 1), (1, 0.7, 0, 1), (1, 0.8, 0, 1), (1, 0.9, 0, 1), (1, 1, 0, 1)
        ]

        i = 10
        for color in colors:
            btn = Button(text=f"Pain intensity value: {i}", background_color=color, font_size="8mm")
            btn.bind(on_release=lambda btn: self.set_color(btn.background_color))
            color_grid.add_widget(btn)
            i -= 1

        popup = Popup(title='Pick a Color', content=color_grid, size_hint=(0.8, 0.8))
        popup.open()
        self.color_picker_popup = popup

    def set_color(self, color):
        self.paint_widget.color = color
        self.color_picker_popup.dismiss()

    def clear_canvas(self, instance):
        self.paint_widget.clear_canvas()

    def save_canvas(self, instance):
        self.paint_widget.save_canvas()

    def go_back(self, instance):
        self.manager.current = 'menu_page'


class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (1, 0, 0, 1)  # Default to red
        self.line_width = 2

        # Load the image
        with self.canvas:
            self.bg = CoreImage('pages/menu_page/seepain_info/human_sketch_2.png').texture
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












'''





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

        # Add the Back button
        back_button = Button(text='Back')
        back_button.bind(on_release=self.go_back)
        button_layout.add_widget(back_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)

    def open_color_picker(self, instance):
        color_grid = BoxLayout(orientation="vertical", spacing=10, size_hint=(1, 1))
        colors = [
            (1, 0, 0, 1), (1, 0.2, 0, 1), (1, 0.3, 0, 1), (1, 0.4, 0, 1), (1, 0.5, 0, 1),
            (1, 0.6, 0, 1), (1, 0.7, 0, 1), (1, 0.8, 0, 1), (1, 0.9, 0, 1), (1, 1, 0, 1)
        ]

        i = 10
        for color in colors:
            btn = Button(text=f"Pain intensity value: {i}", background_color=color, font_size="8mm")
            btn.bind(on_release=lambda btn: self.set_color(btn.background_color))
            color_grid.add_widget(btn)
            i -= 1

        popup = Popup(title='Pick a Color', content=color_grid, size_hint=(0.8, 0.8))
        popup.open()
        self.color_picker_popup = popup

    def set_color(self, color):
        self.paint_widget.color = color
        self.color_picker_popup.dismiss()

    def clear_canvas(self, instance):
        self.paint_widget.clear_canvas()

    def save_canvas(self, instance):
        self.paint_widget.save_canvas()

    def go_back(self, instance):
        self.manager.current = 'new_canvas'  # Navigate back to the main screen


# Assuming this part is in your main file where you set up the screens
class Pain2D(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(NewCanvasScreen(name='new_canvas'))
        sm.add_widget(Pain2D_draw(name='pain2d'))
        sm.add_widget(PatientInfoScreen(name='patient_info'))
        sm.add_widget(QuestionaireInfoScreen(name='questionnaire_info'))
        return sm


if __name__ == '__main__':
    Pain2D().run()




'''


