from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Rectangle, Ellipse
from kivy.properties import BooleanProperty
from kivy.uix.scatter import Scatter
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import os
from kivy.uix.screenmanager import Screen

# Check if we are running on Android
try:
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    android_imported = True
except ImportError:
    android_imported = False
    print("Running on non-Android platform, android-specific features won't work.")


# 1. Drawing Class
class DrawWidget(Scatter):
    is_drawing = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.do_scale = False
        self.do_translation = False
        self.do_rotation = False
        self.line_width = 2
        self.color = (1, 0, 0, 1)
        self.lines = []
        self.colors = []
        self.eraser_enabled = False
        self.undo_stack = []  # Stack to store removed lines for undo
        self.redo_stack = []  # Stack to store undone lines for redo
        self.redo_color_stack = []
        self.undo_color_stack = []
        self.eraser_indicator = None  # To store the reference to the eraser indicator
        self.eraser_size = 30  # Diameter of the eraser indicator circle

        # Add a white background
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Load the background image with correct properties
        self.background_image = Image(source='pages/menu_page/seepain_info/new_template_human_sketch.png',
                                      allow_stretch=True,
                                      keep_ratio=True)
        self.background_image.size_hint_y = None
        self.background_image.height = self.height  # Adjust this to control the image height
        self.background_image.center_x = self.center_x  # Center the image horizontally
        self.add_widget(self.background_image)

    def on_size(self, *args):
        # Update image dimensions when the widget size changes
        self.background_image.width = self.width
        self.background_image.height = self.height
        self.background_image.center_x = self.center_x  # Center image when size changes

        # Update the rectangle size to cover the background
        self.rect.size = self.size

    def on_touch_down(self, touch):
        # Check if the drawing mode is enabled
        if self.is_drawing:
            # Check if the touch is within the widget bounds
            if self.collide_point(*touch.pos):
                with self.canvas:
                    Color(*self.color)  # Set the drawing color

                    # Get the local coordinates using self.to_local
                    local_x, local_y = self.to_local(*touch.pos)

                    if self.eraser_enabled:
                        # Show the eraser indicator
                        if not self.eraser_indicator:
                            with self.canvas:
                                Color(1, 0, 0, 0.5)  # Semi-transparent red color for visibility
                                self.eraser_indicator = Ellipse(pos=(local_x - self.eraser_size / 2, local_y - self.eraser_size / 2),
                                                                size=(self.eraser_size, self.eraser_size))

                        # Eraser functionality
                        for line in self.lines:
                            # Check each segment of the line for proximity to the touch position
                            for i in range(0, len(line['original_points']), 2):
                                if abs(local_x - line['original_points'][i]) < 20 and \
                                        abs(local_y - line['original_points'][i + 1]) < 20:  # Adjust threshold as needed

                                    # Remove the point from the original points
                                    line['original_points'].pop(i)  # Remove corresponding x-coordinate
                                    line['original_points'].pop(i)  # Remove corresponding y-coordinate
                                    self.canvas.remove(line['line'])  # Optionally remove the line from the canvas
                                    self.lines.remove(line)  # Remove line entry
                                    break  # Exit the loop once a point is erased

                    else:
                        # Drawing mode
                        touch.ud["line"] = Line(points=(local_x, local_y), width=self.line_width)
                        # Store original points
                        self.lines.append({
                            'line': touch.ud["line"],
                            'original_points': [local_x, local_y]
                        })
                        self.colors.append(self.color)

                # Clear the redo stack when drawing a new line
                self.redo_stack.clear()
                self.redo_color_stack.clear()
                return True
        else:
            # Handle other touch actions (like moving the image)
            self.do_scale = True
            self.do_translation = True
            super().on_touch_down(touch)

        return True

    def on_touch_move(self, touch):
        if self.is_drawing and "line" in touch.ud:
            touch.ud["line"].points += self.to_local(*touch.pos)

            local_x, local_y = self.to_local(*touch.pos)

            self.lines[-1]['original_points'].extend([local_x, local_y])
        else:
            super().on_touch_move(touch)

    def on_touch_up(self, touch):
        # Remove the eraser indicator when the touch ends
        if self.eraser_indicator:
            self.canvas.remove(self.eraser_indicator)
            self.eraser_indicator = None  # Reset the eraser indicator

        super().on_touch_up(touch)

    def toggle_eraser_mode(self):
        """Method to toggle between move and draw modes"""
        self.eraser_enabled = not self.eraser_enabled

    def clear_canvas(self):

        for i in range(len(self.lines)):
            last_line = self.lines.pop()
            self.undo_stack.append(last_line)
            self.canvas.remove(last_line['line'])

    def undo(self):
        if self.lines:
            last_line = self.lines.pop()
            self.undo_stack.append(last_line)
            self.canvas.remove(last_line['line'])

        if self.colors:
            last_color = self.colors.pop()
            self.undo_color_stack.append(last_color)


    def redo(self):
        if self.undo_stack:
            last_undone_line = self.undo_stack.pop()
            self.lines.append(last_undone_line)

            last_undone_color = self.undo_color_stack.pop()
            self.colors.append(last_undone_color)

            with self.canvas:
                Color(*last_undone_color)
                self.canvas.add(last_undone_line['line'])

    def save_canvas(self, file_path):
        self.export_to_png(file_path)


# 2. Toggle Button Class
class ToggleButton(Button):
    def __init__(self, draw_widget, **kwargs):
        super().__init__(**kwargs)
        self.draw_widget = draw_widget
        self.text = "Zoom/Bewegen"
        self.size_hint = (1, 1)
        self.bind(on_release=self.toggle_mode)

    def toggle_mode(self, instance):
        self.draw_widget.is_drawing = not self.draw_widget.is_drawing
        if self.draw_widget.is_drawing:
            self.text = "Zoom/Bewegen"
            self.background_color = (1, 1, 1, 1)
            self.draw_widget.do_scale = False
            self.draw_widget.do_translation = False
        else:
            self.background_color = (0, 0, 1, 1)
            self.text = "Draw"


# 3. Main Layout Class
class MainLayout(BoxLayout):
    def __init__(self, go_back_callback, **kwargs):
        super().__init__(**kwargs)

        self.go_back_callback = go_back_callback

        self.orientation = "vertical"

        # Add a white background to the main layout
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Drawing area layout
        top_layout = RelativeLayout()
        middle_slider_layout = BoxLayout(orientation="vertical")
        middle_btn_layout = BoxLayout(orientation="horizontal")
        bottom_layout = BoxLayout(orientation="vertical")

        # Set the size_hint for the nested layouts before adding them
        top_layout.size_hint = (1, 0.7)
        middle_slider_layout.size_hint = (1, 0.1)
        middle_btn_layout.size_hint = (1, 0.1)
        bottom_layout.size_hint = (1, 0.1)

        # Initialize the draw widget with the background image
        self.draw_widget = DrawWidget()
        top_layout.add_widget(self.draw_widget)

        # Introduce sliders

        # slider for pencil level
        self.pencil_slider = Slider(min=1, max=10, value=2, orientation='horizontal', value_track=True,
                                    value_track_color=[0.8, 0.8, 0.8, 1])

        self.pencil_value_label = Label(text=str(int(self.pencil_slider.value)), color=(0, 0, 0, 1))

        # Bind the slider's value to both update the label and set the drawing color
        self.pencil_slider.bind(value=lambda instance, value: (
            self.pencil_value_label.setter('text')(self.pencil_value_label, str(int(value))),
            self.set_pencil_thickness(value)
        ))

        # Middle pencil slider nested layout
        middle_pencil_slider_nested_layout = BoxLayout(orientation="horizontal")

        middle_pencil_slider_nested_layout_1 = BoxLayout(orientation="horizontal")
        middle_pencil_slider_nested_layout_2 = BoxLayout(orientation="horizontal")
        middle_pencil_slider_nested_layout_3 = BoxLayout(orientation="horizontal")

        middle_pencil_slider_nested_layout_1.add_widget(Label(text="Bleistiftdicke", color=(0, 0, 0, 1)))
        middle_pencil_slider_nested_layout_2.add_widget(self.pencil_slider)
        middle_pencil_slider_nested_layout_3.add_widget(self.pencil_value_label)

        middle_pencil_slider_nested_layout_1.size_hint = (0.15, 1)
        middle_pencil_slider_nested_layout_2.size_hint = (0.85, 1)
        middle_pencil_slider_nested_layout_3.size_hint = (0.05, 1)

        middle_pencil_slider_nested_layout.add_widget(middle_pencil_slider_nested_layout_1)
        middle_pencil_slider_nested_layout.add_widget(middle_pencil_slider_nested_layout_3)
        middle_pencil_slider_nested_layout.add_widget(middle_pencil_slider_nested_layout_2)

        # Slider for Pain level
        self.pain_slider = Slider(min=1, max=10, value=10, orientation='horizontal', value_track=True,
                                  value_track_color=[1, 0, 0, 1])

        self.pain_value_label = Label(text=str(int(self.pain_slider.value)), color=(0, 0, 0, 1))

        # Bind the slider's value to both update the label and set the drawing color
        self.pain_slider.bind(value=lambda instance, value: (
            self.pain_value_label.setter('text')(self.pain_value_label, str(int(value))),
            self.set_pain_color(value)
        ))

        # Middle2 nested layout
        middle_pain_slider_nested_layout = BoxLayout(orientation="horizontal")

        middle_pain_slider_nested_layout_1 = BoxLayout(orientation="horizontal")
        middle_pain_slider_nested_layout_2 = BoxLayout(orientation="horizontal")
        middle_pain_slider_nested_layout_3 = BoxLayout(orientation="horizontal")

        middle_pain_slider_nested_layout_1.add_widget(Label(text="Schmerzniveau", color=(0, 0, 0, 1)))
        middle_pain_slider_nested_layout_2.add_widget(self.pain_slider)
        middle_pain_slider_nested_layout_3.add_widget(self.pain_value_label)

        middle_pain_slider_nested_layout_1.size_hint = (0.15, 1)
        middle_pain_slider_nested_layout_2.size_hint = (0.85, 1)
        middle_pain_slider_nested_layout_3.size_hint = (0.05, 1)

        middle_pain_slider_nested_layout.add_widget(middle_pain_slider_nested_layout_1)
        middle_pain_slider_nested_layout.add_widget(middle_pain_slider_nested_layout_3)
        middle_pain_slider_nested_layout.add_widget(middle_pain_slider_nested_layout_2)

        # add slider to the middle widget

        middle_slider_layout.add_widget(middle_pencil_slider_nested_layout)
        middle_slider_layout.add_widget(middle_pain_slider_nested_layout)

        # Initialize the toggle button and pass the draw widget to it
        toggle_button = ToggleButton(self.draw_widget)
        middle_btn_layout.add_widget(toggle_button)

        self.eraser_button = Button(text='Radiergummi')
        self.eraser_button.bind(on_release=self.toggle_eraser_mode)
        middle_btn_layout.add_widget(self.eraser_button)

        clear_button = Button(text='   Alles\nLöschen')
        clear_button.bind(on_release=lambda instance: self.draw_widget.clear_canvas())
        middle_btn_layout.add_widget(clear_button)

        undo_button = Button(text="Rückgängig")
        undo_button.bind(on_release=lambda instance: self.draw_widget.undo())
        middle_btn_layout.add_widget(undo_button)

        redo_button = Button(text="Wiederherstellen")
        redo_button.bind(on_release=lambda instance: self.draw_widget.redo())
        middle_btn_layout.add_widget(redo_button)

        help_btn = Button(text="Helfen")
        help_btn.bind(on_press=self.show_help)
        middle_btn_layout.add_widget(help_btn)

        # Add bottom buttons

        btn_submit = Button(text="Einreichen", background_color=(0, 1, 0, 1))
        btn_submit.bind(on_press=self.show_save_popup)
        btn_back = Button(text="Zurück", background_color=(1, 0, 0, 1))
        btn_back.bind(on_press=self.go_back_callback)

        bottom_layout.add_widget(btn_submit)
        bottom_layout.add_widget(btn_back)



        # Add widgets to the layout
        self.add_widget(top_layout)
        self.add_widget(middle_slider_layout)
        self.add_widget(middle_btn_layout)
        self.add_widget(bottom_layout)

        # Request permissions if on Android
        if android_imported:
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        # Add all the functions

    def on_size(self, *args):
        # Update the rectangle size to cover the background of the main layout
        self.rect.size = self.size
        self.rect.pos = self.pos

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
        self.draw_widget.line_width = value
        self.pencil_slider.value_track_color = color_values[index]

    def set_pain_color(self, value):
        """Update the pencil color and slider track color based on the pain slider value."""
        color_values = [
            (1, 1, 0, 1),  # yellow
            (1, 0.9, 0, 1),
            (1, 0.8, 0, 1),
            (1, 0.7, 0, 1),
            (1, 0.6, 0, 1),
            (1, 0.5, 0, 1),
            (1, 0.4, 0, 1),
            (1, 0.3, 0, 1),
            (1, 0.2, 0, 1),
            (1, 0, 0, 1),  # red
        ]
        # Calculate the index for the color based on the slider value
        index = int(value) - 1
        self.draw_widget.color = color_values[index]
        self.pain_slider.value_track_color = color_values[index]

    def toggle_eraser_mode(self, instance):
        """Toggle eraser/draw mode and change the button color"""
        self.draw_widget.toggle_eraser_mode()
        if self.draw_widget.eraser_enabled:
            self.eraser_button.background_color = (0, 0, 1, 1)  # Blue for eraser mode
        else:
            self.eraser_button.background_color = (1, 1, 1, 1)  # White for draw mode

    def show_help(self, instance):
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(
            Label(text="Abkürzungen:\n \nV: Vorne \nH: Hinten  \nL: Links \nR: Rechts"))

        popup = Popup(title="Helfen", content=popup_layout, size_hint=(0.5, 0.5))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'menu_page'

    def show_save_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)

        self.file_name_input = TextInput(hint_text='Geben Sie Ihr Pseudonym ein.')
        content.add_widget(self.file_name_input)

        save_button = Button(text='Speichern', size_hint_y=None, height=100, background_color = (0, 1, 0, 1))
        save_button.bind(on_press=self.save_canvas_with_name)
        content.add_widget(save_button)

        self.save_popup = Popup(title='Bild Speichern', content=content, size_hint=(0.8, 0.4))
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
                # Save the canvas after resetting the zoom
                self.draw_widget.save_canvas(save_path)
                print(f"Image saved successfully at: {save_path}")

                # Show success message in German
                self.show_success_popup("Bild erfolgreich gespeichert!", "Schließen")

                # Close the popup
                self.save_popup.dismiss()
            except Exception as e:
                print(f"Error saving image: {str(e)}")
        else:
            print("No file name provided.")

    def show_success_popup(self, message, button_text):
        content = BoxLayout(orientation='vertical')
        label = Label(text=message)
        close_button = Button(text=button_text, background_color=(1, 0, 0, 1))

        close_button.bind(on_release=self.close_app)  # Bind close button to close_app method

        content.add_widget(label)
        content.add_widget(close_button)

        success_popup = Popup(title='Erfolg', content=content, size_hint=(0.8, 0.4))
        success_popup.open()

    def close_app(self, instance):
        App.get_running_app().stop()  # Stop the app


class SeePainPage(Screen):
    def __init__(self, **kwargs):
        super(SeePainPage, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.main_layout = MainLayout(go_back_callback=self.go_back)
        self.add_widget(self.main_layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def go_back(self, instance):
        self.manager.current = 'menu_page'  # Switch to menu page



# 4. Main App Class
class MyApp(App):
    def build(self):
        return SeePainPage()


if __name__ == "__main__":
    MyApp().run()
