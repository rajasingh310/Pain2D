from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput
from kivy.utils import platform

from ...base_page.base_page import BasePage

import os


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

        help_btn = Button(text="Help")
        help_btn.bind(on_press=self.show_help)
        middle_nested_layout.add_widget(help_btn)

        # Bottom nested layout with 1 column and 2 rows
        bottom_nested_layout = GridLayout(cols=1, rows=2)

        btn_submit = Button(text="Submit", background_color=(0, 1, 0, 1))
        btn_submit.bind(on_release=self.save_drawing)
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

    def show_help(self, instance):
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(Label(text="B: Back \nF: Front \nH: Head \nL: Left \nR: Right \nM:Mouth"))

        popup = Popup(title="Help", content=popup_layout, size_hint=(0.8, 0.5))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'menu_page'

    def save_drawing(self, instance):
        # Open a popup to ask for a file name
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="Enter file name:"))

        self.filename_input = TextInput(multiline=False, hint_text="filename")
        layout.add_widget(self.filename_input)

        btn_layout = BoxLayout(orientation='horizontal')
        btn_ok = Button(text="OK", on_release=self.save_image_with_name)
        btn_cancel = Button(text="Cancel", on_release=self.dismiss_popup)
        btn_layout.add_widget(btn_ok)
        btn_layout.add_widget(btn_cancel)

        layout.add_widget(btn_layout)

        self.popup = Popup(title="Save Image", content=layout, size_hint=(0.8, 0.4))
        self.popup.open()

    def dismiss_popup(self, instance):
        self.popup.dismiss()

    def save_image_with_name(self, instance):
        file_name = self.filename_input.text.strip()
        if not file_name:
            # Handle empty filename case
            return

        # Define directory path
        directory = os.path.join(App.get_running_app().user_data_dir, 'Drawings')
        if platform == 'android':
            from android.storage import primary_external_storage_path
            directory = os.path.join(primary_external_storage_path(), 'Drawings')

        # Create the directory if it does not exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, f"{file_name}.png")

        # Check if file exists
        if os.path.exists(file_path):
            # Prompt for overwrite or new name
            layout = BoxLayout(orientation='vertical', padding=10)
            layout.add_widget(Label(text=f"File '{file_name}.png' already exists. Do you want to replace it?"))

            btn_layout = BoxLayout(orientation='horizontal')
            btn_replace = Button(text="Replace", on_release=lambda x: self.save_image(file_path, overwrite=True))
            btn_new_name = Button(text="New Name", on_release=self.save_drawing)
            btn_layout.add_widget(btn_replace)
            btn_layout.add_widget(btn_new_name)

            layout.add_widget(btn_layout)

            self.popup.dismiss()
            self.popup = Popup(title="File Exists", content=layout, size_hint=(0.8, 0.4))
            self.popup.open()
        else:
            self.save_image(file_path)

    def save_image(self, file_path, overwrite=False):
        # Save the current canvas as a PNG file
        self.paint_widget.export_to_png(file_path)

        if not overwrite:
            self.popup.dismiss()

        # Notify the user that the image has been saved
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text=f"Image saved as '{os.path.basename(file_path)}'"))

        btn_ok = Button(text="OK", on_release=self.dismiss_popup)
        layout.add_widget(btn_ok)

        self.popup = Popup(title="Saved", content=layout, size_hint=(0.8, 0.3))
        self.popup.open()


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

