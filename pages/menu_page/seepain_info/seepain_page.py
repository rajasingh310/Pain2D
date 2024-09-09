from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from ...base_page.base_page import BasePage  # Make sure your BasePage is correctly referenced


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


class SeePainPage(BasePage):
    def __init__(self, **kwargs):
        super(SeePainPage, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation="vertical")

        # Top nested layout
        top_nested_layout = BoxLayout(orientation="horizontal")

        # Left side slider for zoom
        self.zoom_slider = Slider(min=0.5, max=3, value=1, orientation='vertical', size_hint=(0.1, 1))
        self.zoom_slider.bind(value=lambda instance, value: self.paint_widget.set_zoom(value))
        top_nested_layout.add_widget(self.zoom_slider)

        # The drawing widget
        self.paint_widget = PaintWidget()
        top_nested_layout.add_widget(self.paint_widget)

        # Middle nested layout
        middle_nested_layout = BoxLayout(orientation="horizontal")

        color_picker_button = Button(text='Pain Indicator')
        color_picker_button.bind(on_release=self.open_color_picker)
        middle_nested_layout.add_widget(color_picker_button)

        clear_button = Button(text='Clear')
        clear_button.bind(on_release=self.clear_canvas)
        middle_nested_layout.add_widget(clear_button)

        undo_button = Button(text="Undo")
        undo_button.bind(on_release=lambda instance: self.paint_widget.undo())
        middle_nested_layout.add_widget(undo_button)

        redo_button = Button(text="Redo")
        redo_button.bind(on_release=lambda instance: self.paint_widget.redo())
        middle_nested_layout.add_widget(redo_button)

        # Extra Button for toggling move/draw mode
        self.toggle_move_button = Button(text="Toggle Move/Draw", background_color=(1, 1, 1, 1))
        self.toggle_move_button.bind(on_release=self.toggle_move_mode)
        middle_nested_layout.add_widget(self.toggle_move_button)

        help_btn = Button(text="Help")
        help_btn.bind(on_press=self.show_help)
        middle_nested_layout.add_widget(help_btn)

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
            btn = Button(text=f"Pain intensity value: {i}", background_color=color)
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

    def toggle_move_mode(self, instance):
        """Toggle move/draw mode and change the button color"""
        self.paint_widget.toggle_move_mode()
        if self.paint_widget.move_enabled:
            self.toggle_move_button.background_color = (0, 0, 1, 1)  # Green for move mode
        else:
            self.toggle_move_button.background_color = (1, 1, 1, 1)  # Default color for draw mode
