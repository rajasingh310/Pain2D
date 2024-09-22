from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.graphics import Fbo, ClearColor, ClearBuffers
from ...base_page.base_page import BasePage  # Ensure BasePage is correctly referenced
import os
from kivy.uix.textinput import TextInput

# Check if we are running on Android
try:
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    android_imported = True
except ImportError:
    android_imported = False
    print("Running on non-Android platform, android-specific features won't work.")


class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (1, 0, 0, 1)  # Default drawing color: red
        self.line_width = 2
        self.zoom_scale = 1.0
        self.is_moving = False  # Flag to track whether we are in move mode
        self.move_enabled = False  # To toggle between move and draw mode
        self.last_touch_pos = None  # To track the last position for moving

        # To store lines and their original points for transformation
        self.lines = []
        self.undo_stack = []  # Stack to store removed lines for undo
        self.redo_stack = []  # Stack to store undone lines for redo

        # Load the image
        self.bg_image = CoreImage('pages/menu_page/seepain_info/human_sketch_2.png').texture
        self.img_aspect_ratio = self.bg_image.width / self.bg_image.height  # Aspect ratio of the image

        with self.canvas:
            self.rect = Rectangle(texture=self.bg_image, pos=self.pos, size=self.size)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        # Calculate the aspect ratio of the widget
        widget_aspect_ratio = self.width / self.height

        # If the widget is wider than the image's aspect ratio, scale based on height
        if widget_aspect_ratio > self.img_aspect_ratio:
            new_height = self.height * self.zoom_scale
            new_width = new_height * self.img_aspect_ratio
        else:
            # Otherwise, scale based on width
            new_width = self.width * self.zoom_scale
            new_height = new_width / self.img_aspect_ratio

        # Center the image in the widget
        self.rect.size = (new_width, new_height)
        self.rect.pos = (
            self.center_x - new_width / 2,
            self.center_y - new_height / 2
        )

        # Update the lines to match the new image position and scale
        self.update_lines()

    def update_lines(self):
        """Updates the lines according to the current zoom scale and position of the image."""
        for line_data in self.lines:
            original_points = line_data['original_points']
            scaled_points = []
            for i in range(0, len(original_points), 2):
                # Apply zoom and translation to the points
                x = self.rect.pos[0] + (original_points[i] * self.rect.size[0])
                y = self.rect.pos[1] + (original_points[i + 1] * self.rect.size[1])
                scaled_points.extend([x, y])

            # Update the points of the line
            line_data['line'].points = scaled_points

    def on_touch_down(self, touch):
        if self.move_enabled:
            # Start moving the image
            self.last_touch_pos = touch.pos
            self.is_moving = True
            return True
        else:
            # Drawing mode
            if self.collide_point(*touch.pos):
                with self.canvas:
                    Color(*self.color)
                    # Normalize the touch positions relative to the image
                    normalized_x = (touch.x - self.rect.pos[0]) / self.rect.size[0]
                    normalized_y = (touch.y - self.rect.pos[1]) / self.rect.size[1]
                    touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)
                    # Store original normalized points
                    self.lines.append({
                        'line': touch.ud['line'],
                        'original_points': [normalized_x, normalized_y]
                    })
                # Clear the redo stack when drawing a new line
                self.redo_stack.clear()
                return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.move_enabled and self.is_moving:
            # Move the image
            if self.last_touch_pos:
                dx = touch.x - self.last_touch_pos[0]
                dy = touch.y - self.last_touch_pos[1]
                self.rect.pos = (self.rect.pos[0] + dx, self.rect.pos[1] + dy)
                self.last_touch_pos = touch.pos
                self.update_lines()
            return True
        elif 'line' in touch.ud:
            # Drawing mode
            touch.ud['line'].points += [touch.x, touch.y]
            # Normalize the points as they are being drawn
            normalized_x = (touch.x - self.rect.pos[0]) / self.rect.size[0]
            normalized_y = (touch.y - self.rect.pos[1]) / self.rect.size[1]
            self.lines[-1]['original_points'].extend([normalized_x, normalized_y])
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        # Reset the move flag when the touch is released
        if self.is_moving:
            self.is_moving = False
            self.last_touch_pos = None
        return super().on_touch_up(touch)

    def clear_canvas(self):
        self.canvas.clear()
        with self.canvas:
            self.rect = Rectangle(texture=self.bg_image, pos=self.rect.pos, size=self.rect.size)
        self.lines.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()

    def set_zoom(self, value):
        """Method to be linked with the zoom slider to update zoom level"""
        self.zoom_scale = value
        self.update_rect()

    def toggle_move_mode(self):
        """Method to toggle between move and draw modes"""
        self.move_enabled = not self.move_enabled

    def undo(self):
        if self.lines:
            last_line = self.lines.pop()
            self.undo_stack.append(last_line)
            self.canvas.remove(last_line['line'])

    def redo(self):
        if self.undo_stack:
            last_undone_line = self.undo_stack.pop()
            self.lines.append(last_undone_line)
            with self.canvas:
                Color(*self.color)
                self.canvas.add(last_undone_line['line'])

    def save_canvas(self, file_path):
        self.export_to_png(file_path)




class SeePainPage(BasePage):
    def __init__(self, **kwargs):
        super(SeePainPage, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation="vertical")

        # Top nested layout
        top_nested_layout = BoxLayout(orientation="vertical")

        # The drawing widget
        self.paint_widget = PaintWidget()
        top_nested_layout.add_widget(self.paint_widget)

        # slider for zoom
        self.zoom_slider = Slider(min=1, max=10, value=1, orientation='horizontal', value_track=True, value_track_color=[1, 1, 0, 1])
        self.zoom_value_label = Label(text=str(int(self.zoom_slider.value)), color=(0, 0, 0, 1))

        # Bind the slider's value to both update the label and set the drawing color
        self.zoom_slider.bind(value=lambda instance, value: (
            self.zoom_value_label.setter('text')(self.zoom_value_label, str(int(value))),
            self.set_zoom_color(value)
        ))



        # Middle1 nested layout
        middle1_nested_layout = BoxLayout(orientation="horizontal")

        middle11_nested_layout = BoxLayout(orientation="horizontal")
        middle12_nested_layout = BoxLayout(orientation="horizontal")
        middle13_nested_layout = BoxLayout(orientation="horizontal")

        middle11_nested_layout.add_widget(Label(text="Zoom", color=(0, 0, 0, 1)))
        middle12_nested_layout.add_widget(self.zoom_slider)
        middle13_nested_layout.add_widget(self.zoom_value_label)

        middle11_nested_layout.size_hint = (0.15, 1)
        middle12_nested_layout.size_hint = (0.85, 1)
        middle13_nested_layout.size_hint = (0.05, 1)

        middle1_nested_layout.add_widget(middle11_nested_layout)
        middle1_nested_layout.add_widget(middle13_nested_layout)
        middle1_nested_layout.add_widget(middle12_nested_layout)

        # slider for pain level
        self.pain_slider = Slider(min=1, max=10, value=10, orientation='horizontal', value_track=True,
                                  value_track_color=[1, 0, 0, 1])

        self.pain_value_label = Label(text=str(int(self.pain_slider.value)), color=(0, 0, 0, 1))

        # Bind the slider's value to both update the label and set the drawing color
        self.pain_slider.bind(value=lambda instance, value: (
            self.pain_value_label.setter('text')(self.pain_value_label, str(int(value))),
            self.set_pain_color(value)
        ))

        # Middle2 nested layout
        middle2_nested_layout = BoxLayout(orientation="horizontal")

        middle21_nested_layout = BoxLayout(orientation="horizontal")
        middle22_nested_layout = BoxLayout(orientation="horizontal")
        middle23_nested_layout = BoxLayout(orientation="horizontal")

        middle21_nested_layout.add_widget(Label(text="Schmerzniveau", color=(0, 0, 0, 1)))
        middle22_nested_layout.add_widget(self.pain_slider)
        middle23_nested_layout.add_widget(self.pain_value_label)

        middle21_nested_layout.size_hint = (0.15, 1)
        middle22_nested_layout.size_hint = (0.85, 1)
        middle23_nested_layout.size_hint = (0.05, 1)

        middle2_nested_layout.add_widget(middle21_nested_layout)
        middle2_nested_layout.add_widget(middle23_nested_layout)
        middle2_nested_layout.add_widget(middle22_nested_layout)

        # slider for pain level
        self.pencil_slider = Slider(min=1, max=10, value=2, orientation='horizontal', value_track=True,
                                  value_track_color=[0.8, 0.8, 0.8, 1])

        self.pencil_value_label = Label(text=str(int(self.pencil_slider.value)), color=(0, 0, 0, 1))

        # Bind the slider's value to both update the label and set the drawing color
        self.pencil_slider.bind(value=lambda instance, value: (
            self.pencil_value_label.setter('text')(self.pencil_value_label, str(int(value))),
            self.set_pencil_thickness(value)
        ))

        # Middle3 nested layout
        middle3_nested_layout = BoxLayout(orientation="horizontal")

        middle31_nested_layout = BoxLayout(orientation="horizontal")
        middle32_nested_layout = BoxLayout(orientation="horizontal")
        middle33_nested_layout = BoxLayout(orientation="horizontal")

        middle31_nested_layout.add_widget(Label(text="Bleistiftdicke", color=(0, 0, 0, 1)))
        middle32_nested_layout.add_widget(self.pencil_slider)
        middle33_nested_layout.add_widget(self.pencil_value_label)

        middle31_nested_layout.size_hint = (0.15, 1)
        middle32_nested_layout.size_hint = (0.85, 1)
        middle33_nested_layout.size_hint = (0.05, 1)

        middle3_nested_layout.add_widget(middle31_nested_layout)
        middle3_nested_layout.add_widget(middle33_nested_layout)
        middle3_nested_layout.add_widget(middle32_nested_layout)

        # Middle nested layout
        middle_nested_layout = BoxLayout(orientation="horizontal")

        clear_button = Button(text='Löschen')
        clear_button.bind(on_release=self.clear_canvas)
        middle_nested_layout.add_widget(clear_button)

        undo_button = Button(text="Undo")
        undo_button.bind(on_release=lambda instance: self.paint_widget.undo())
        middle_nested_layout.add_widget(undo_button)

        redo_button = Button(text="Redo")
        redo_button.bind(on_release=lambda instance: self.paint_widget.redo())
        middle_nested_layout.add_widget(redo_button)

        # Extra Button for toggling move/draw mode
        self.toggle_move_button = Button(text="Bewegen/Ziehen", background_color=(1, 1, 1, 1))
        self.toggle_move_button.bind(on_release=self.toggle_move_mode)

        middle_nested_layout.add_widget(self.toggle_move_button)

        help_btn = Button(text="Helfen")
        help_btn.bind(on_press=self.show_help)
        middle_nested_layout.add_widget(help_btn)

        # Bottom nested layout with 1 column and 2 rows
        bottom_nested_layout = GridLayout(cols=1, rows=2)

        btn_submit = Button(text="Einreichen", background_color=(0, 1, 0, 1))
        btn_submit.bind(on_press=self.show_save_popup)
        btn_back = Button(text="Zurück", background_color=(1, 0, 0, 1))

        btn_back.bind(on_press=self.go_back)

        bottom_nested_layout.add_widget(btn_submit)
        bottom_nested_layout.add_widget(btn_back)

        # Set the size_hint for the nested layouts before adding them
        top_nested_layout.size_hint = (1, 0.65)
        middle1_nested_layout.size_hint = (1, 0.05)
        middle2_nested_layout.size_hint = (1, 0.05)
        middle3_nested_layout.size_hint = (1, 0.05)
        middle_nested_layout.size_hint = (1, 0.1)
        bottom_nested_layout.size_hint = (1, 0.1)

        # Add nested layouts to the main layout
        main_layout.add_widget(top_nested_layout)
        main_layout.add_widget(middle1_nested_layout)
        main_layout.add_widget(middle2_nested_layout)
        main_layout.add_widget(middle3_nested_layout)
        main_layout.add_widget(middle_nested_layout)
        main_layout.add_widget(bottom_nested_layout)

        self.add_widget(main_layout)

        # Request permissions if on Android
        if android_imported:
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])


    def set_pain_color(self, value):
        """Update the pencil color and slider track color based on the pain slider value."""
        color_values = [
            (1, 1, 0, 1),   # yellow
            (1, 0.9, 0, 1),
            (1, 0.8, 0, 1),
            (1, 0.7, 0, 1),
            (1, 0.6, 0, 1),
            (1, 0.5, 0, 1),
            (1, 0.4, 0, 1),
            (1, 0.3, 0, 1),
            (1, 0.2, 0, 1),
            (1, 0, 0, 1),   # red
        ]
        # Calculate the index for the color based on the slider value
        index = int(value) - 1
        self.paint_widget.color = color_values[index]
        self.pain_slider.value_track_color = color_values[index]

    def set_zoom_color(self, value):
        """Update the pencil color and slider track color based on the pain slider value."""
        color_values = [
            (0, 1, 0, 1),  # green
            (0, 0.9, 0.1, 1),
            (0, 0.8, 0.2, 1),
            (0, 0.7, 0.3, 1),
            (0, 0.6, 0.4, 1),
            (0, 0.5, 0.5, 1),  # green-blue blend
            (0, 0.4, 0.6, 1),
            (0, 0.3, 0.7, 1),
            (0, 0.2, 0.8, 1),
            (0, 0, 1, 1)  # blue
        ]
        # Calculate the index for the color based on the slider value
        index = int(value) - 1
        self.paint_widget.set_zoom(value)
        self.zoom_slider.value_track_color = color_values[index]

    def set_pencil_thickness(self, value):
        """Update the pencil color and slider track color based on the pain slider value."""
        # Define grayscale colors from light gray to dark black
        color_values = [
            (0.85, 0.85, 0.85, 1),  # light gray
            (0.8, 0.8, 0.8, 1),
            (0.7, 0.7, 0.7, 1),
            (0.6, 0.6, 0.6, 1),
            (0.5, 0.5, 0.5, 1),
            (0.4, 0.4, 0.4, 1),
            (0.3, 0.3, 0.3, 1),
            (0.2, 0.2, 0.2, 1),
            (0.1, 0.1, 0.1, 1),
            (0, 0, 0, 1)  # black
        ]

        # Calculate the index for the color based on the slider value
        index = int(value) - 1
        self.paint_widget.line_width = value
        self.pencil_slider.value_track_color = color_values[index]

    def clear_canvas(self, instance):
        self.paint_widget.clear_canvas()

    def show_help(self, instance):
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(Label(text="Abkürzungen:\n \nB: Rücken \nF: Vorderseite \nH: Kopf \nL: Links \nR: Rechts \nM: Mund "))

        popup = Popup(title="Helfen", content=popup_layout, size_hint=(0.5, 0.5))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'menu_page'

    def toggle_move_mode(self, instance):
        """Toggle move/draw mode and change the button color"""
        self.paint_widget.toggle_move_mode()
        if self.paint_widget.move_enabled:
            self.toggle_move_button.background_color = (0, 0, 1, 1)  # Blue for move mode
        else:
            self.toggle_move_button.background_color = (1, 1, 1, 1)  # White for draw mode

    def show_save_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)

        self.file_name_input = TextInput(hint_text='Enter file name')
        content.add_widget(self.file_name_input)

        save_button = Button(text='Save', size_hint_y=None, height=50)
        save_button.bind(on_press=self.save_canvas_with_name)
        content.add_widget(save_button)

        self.save_popup = Popup(title='Save Image', content=content, size_hint=(0.8, 0.4))
        self.save_popup.open()

    def save_canvas_with_name(self, instance):
        file_name = self.file_name_input.text.strip()
        if file_name:
            if android_imported:
                # Save to Android's primary external storage directory
                storage_path = primary_external_storage_path()
                save_path = os.path.join(storage_path, 'Download', f'{file_name}.png')
            else:
                # Save to the current working directory for testing on PC
                save_path = os.path.join(os.getcwd(), f'{file_name}.png')

            try:
                # Reset zoom value to default (1.0)
                self.paint_widget.set_zoom(1.0)
                # Save the canvas after resetting the zoom
                self.paint_widget.save_canvas(save_path)
                print(f"Image saved successfully at: {save_path}")

                # Close the popup
                self.save_popup.dismiss()
            except Exception as e:
                print(f"Error saving image: {str(e)}")
        else:
            print("No file name provided.")