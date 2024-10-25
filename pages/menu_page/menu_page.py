from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from ..base_page.base_page import BasePage
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel


class MenuPage(BasePage):
    def __init__(self, **kwargs):
        super(MenuPage, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation="vertical")

        # Top Nested Layout with Carousel
        top_nested_layout = BoxLayout(orientation="vertical")
        carousel = Carousel(direction='right', loop=True)  # Carousel to swipe between images/text

        # List of image paths and corresponding texts
        image_text_data = [
            {'image': 'pages/menu_page/pen_tablet.png', 'text': "1/6 \nNutzen Sie den beim Tablett liegenden Stift zum Zeichnen."},
            {'image': 'pages/menu_page/pen_thickness.png', 'text': "2/6 \nSie können die Bleistiftdicke mit dem Regler nach Wunsch anpassen."},
            {'image': 'pages/menu_page/pain_value.png', 'text': "3/6 \nSie können verschiedene Schmerzintensitäten angeben."},
            {'image': 'pages/menu_page/info.png', 'text': "4/6 \nWie man Pain Drawings richtig ausfüllt!"},
            {'text': "5/6 \nWenn Sie fertig sind, drücken Sie auf Einreichen und geben Ihr Pseudonym ein. \n\nFalls sie dies nicht wissen, geben sie Name und Geburtsdatum an. \n\nAnschließend füllen Sie den Fragebogen aus."},  # Slide with only text
            {'text': "6/6 \nZeichnen Sie nun Ihren durchschnittlichen Schmerz der letzten Woche in die Person ein."}
        ]

        for item in image_text_data:
            slide_layout = BoxLayout(orientation="vertical")

            # Add Label for text
            label = Label(
                text=item['text'],
                font_size="25sp",
                color=(0, 0, 0, 1),
                size_hint_y=0.2,
                halign="center",  # Center align the text horizontally
                valign="middle",  # Center align the text vertically
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
            carousel.add_widget(slide_layout)

        top_nested_layout.add_widget(carousel)

        # Add instruction label to indicate swiping
        swipe_label = Label(text="Streichen Sie, um mehr zu sehen.", font_size="20sp", color=(0, 0, 0, 0.7), size_hint_y=0.05)
        top_nested_layout.add_widget(swipe_label)

        # Middle Nested Layout with Start Button
        middle_nested_layout = BoxLayout(orientation="vertical")

        # Commented code
        # btn1 = Button(text="Patient Info")
        # btn2 = Button(text="Questionnaire Info")
        # btn3 = Button(text="Laboratory Info")
        btn4 = Button(text="Start", background_color=(0, 1, 0, 1))

        # Commented out bind functions for unused buttons
        # btn1.bind(on_press=self.go_to_patient_page)
        # btn2.bind(on_press=self.go_to_questionnaire_page)
        # btn3.bind(on_press=self.go_to_laboratory_page)
        btn4.bind(on_press=self.go_to_seepain_page)

        # middle_nested_layout.add_widget(btn1)
        # middle_nested_layout.add_widget(btn2)
        # middle_nested_layout.add_widget(btn3)
        middle_nested_layout.add_widget(btn4)

        # Bottom Nested Layout with Back Button
        bottom_nested_layout = BoxLayout(orientation="vertical")

        # Commented code
        # btn5 = Button(text="Submit", background_color=(0, 1, 0, 1))
        btn6 = Button(text="Zurück", background_color=(1, 0, 0, 1))

        # Commented out bind function for unused button
        # btn5.bind(on_press=self.submit_form)
        btn6.bind(on_press=self.go_back)

        # bottom_nested_layout.add_widget(btn5)
        bottom_nested_layout.add_widget(btn6)

        # Set size hints for layout positioning
        top_nested_layout.size_hint = (1, 0.8)
        middle_nested_layout.size_hint = (1, 0.1)
        bottom_nested_layout.size_hint = (1, 0.1)

        # Add layouts to main layout
        main_layout.add_widget(top_nested_layout)
        main_layout.add_widget(middle_nested_layout)
        main_layout.add_widget(bottom_nested_layout)

        self.add_widget(main_layout)

    # Commented out unnecessary functions
    # def go_to_patient_page(self, instance):
    #     self.manager.current = 'patient_page'

    # def go_to_questionnaire_page(self, instance):
    #     self.manager.current = 'questionnaire_page'

    # def go_to_laboratory_page(self, instance):
    #     self.manager.current = 'laboratory_page'

    # def submit_form(self, instance):
    #     print("Form Submitted")
    #     # Add functionality here for form submission

    def go_to_seepain_page(self, instance):
        self.manager.current = 'seepain_page'

    def go_back(self, instance):
        self.manager.current = 'first_page'


class MyApp(App):
    def build(self):
        return MenuPage()


if __name__ == "__main__":
    MyApp().run()
