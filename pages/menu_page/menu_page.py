from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from ..base_page.base_page import BasePage
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel


class MenuPage(BasePage):
    def __init__(self, **kwargs):
        super(MenuPage, self).__init__(**kwargs)

        self.start_button_enabled = False  # Start button initial state

        main_layout = BoxLayout(orientation="vertical")

        # Top Nested Layout with Carousel
        top_nested_layout = BoxLayout(orientation="vertical")
        self.carousel = Carousel(direction='right', loop=False)  # Set loop to False

        # List of image paths and corresponding texts
        self.image_text_data = [
            {'image': 'pages/menu_page/pen_tablet.png', 'text': "Nutzen Sie den beim Tablett liegenden Stift zum Zeichnen."},
            {'image': 'pages/menu_page/pen_thickness.png', 'text': "Sie können die Bleistiftdicke mit dem Regler nach Wunsch anpassen."},
            {'image': 'pages/menu_page/pain_value.png', 'text': "Sie können verschiedene Schmerzintensitäten angeben."},
            {'image': 'pages/menu_page/info.png', 'text': "Wie man Pain Drawings richtig ausfüllt!"},
            {'text': "Wenn Sie fertig sind, drücken Sie auf Einreichen und geben Ihr Pseudonym ein. \n\nFalls sie dies nicht wissen, geben sie Name und Geburtsdatum an. \n\nAnschließend füllen Sie den Fragebogen aus."},  # Slide with only text
            {'text': "Zeichnen Sie nun Ihren durchschnittlichen Schmerz \nder letzten Woche in die Person ein."}
        ]

        for item in self.image_text_data:
            slide_layout = BoxLayout(orientation="vertical")

            # Add Label for text
            label = Label(
                text=item['text'],
                font_size="25sp",
                color=(0, 0, 0, 1),
                size_hint_y=0.2,
                halign="center",
                valign="middle",
                text_size=(self.width, None)  # Allow text to wrap
            )
            label.bind(size=label.setter('text_size'))  # Bind size to text_size for wrapping
            slide_layout.add_widget(label)

            # Only add image if it exists in the item dictionary
            if 'image' in item:
                image_texture = CoreImage(item['image']).texture
                image_widget = KivyImage()
                image_widget.texture = image_texture
                image_widget.size_hint_y = 1
                slide_layout.add_widget(image_widget)

            # Add each slide (with text and optional image) to the carousel
            self.carousel.add_widget(slide_layout)

            # Bind the carousel's on_index property to check the button state
        self.carousel.bind(current_slide=self.check_button_state)

        top_nested_layout.add_widget(self.carousel)

        # Add instruction label to indicate swiping
        swipe_label = Label(text="Streichen Sie, um mehr zu sehen.", font_size="20sp", color=(0, 0, 0, 0.7), size_hint_y=0.05)
        top_nested_layout.add_widget(swipe_label)

        # Create a BoxLayout for button indicators
        self.indicator_layout = BoxLayout(
            orientation='horizontal'
        )
        self.indicator_layout.size_hint = (1, 0.025)

        self.buttons = []

        # Create buttons as indicators
        for i in range(len(self.image_text_data)):
            button = Button()  # Fixed width for buttons
            self.buttons.append(button)
            self.indicator_layout.add_widget(button)

            # Fill the first button with green
            if i == 0:
                button.background_color = (0, 1, 0, 1)  # Green color for the first button
            else:
                button.background_color = (1, 1, 1, 1)  # White color for other buttons

        # Middle Nested Layout with Start Button
        middle_nested_layout = BoxLayout(orientation="vertical")

        # Previously commented buttons
        # btn1 = Button(text="Patient Info")
        # btn2 = Button(text="Questionnaire Info")
        # btn3 = Button(text="Laboratory Info")
        self.start_button = Button(text="Start")

        # Bind functions for the previously commented buttons
        # btn1.bind(on_press=self.go_to_patient_page)
        # btn2.bind(on_press=self.go_to_questionnaire_page)
        # btn3.bind(on_press=self.go_to_laboratory_page)
        self.start_button.bind(on_press=self.on_button_click)
        # Set initial button color to dim
        self.update_button_color(False)

        # Add buttons to the layout
        # middle_nested_layout.add_widget(btn1)
        # middle_nested_layout.add_widget(btn2)
        # middle_nested_layout.add_widget(btn3)
        middle_nested_layout.add_widget(self.start_button)

        # Bottom Nested Layout with Back Button
        bottom_nested_layout = BoxLayout(orientation="vertical")

        btn6 = Button(text="Zurück", background_color=(1, 0, 0, 1))
        btn6.bind(on_press=self.go_back)

        bottom_nested_layout.add_widget(btn6)

        # Set size hints for layout positioning
        top_nested_layout.size_hint = (1, 0.8)
        middle_nested_layout.size_hint = (1, 0.075)
        bottom_nested_layout.size_hint = (1, 0.075)

        # Add layouts to main layout
        main_layout.add_widget(top_nested_layout)
        main_layout.add_widget(self.indicator_layout)
        main_layout.add_widget(middle_nested_layout)
        main_layout.add_widget(bottom_nested_layout)

        self.add_widget(main_layout)

    def on_button_click(self, instance):
        # Check if we are on the last slide
        if self.carousel.index == len(self.image_text_data) - 1:
            self.go_to_seepain_page(instance)
        else:
            # Create a popup indicating the user needs to complete the swipe
            popup = Popup(title='Unvollständiger Wischvorgang', content=Label(text='Bitte vervollständigen Sie den Wischvorgang.'),
                          size_hint=(0.6, 0.4))
            popup.open()

    def update_button_color(self, is_final_slide):
        # Update button color based on the slide status
        if is_final_slide:
            self.start_button.background_color = (0, 1, 0, 1)  # Normal color (green)
        else:
            self.start_button.background_color = (0.5, 0.5, 0.5, 1)  # Dim color (gray)

    def check_button_state(self, carousel, slide):
        # Check if the carousel is on the last slide
        is_final_slide = self.carousel.index == len(self.image_text_data) - 1
        self.update_button_color(is_final_slide)

        # Fill the button indicators based on the current index
        for i, button in enumerate(self.buttons):
            if i <= self.carousel.index:
                button.background_color = (0, 1, 0, 1)  # Fill with green
            else:
                button.background_color = (1, 1, 1, 1)  # Reset to white

    # Previously commented out navigation functions
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


