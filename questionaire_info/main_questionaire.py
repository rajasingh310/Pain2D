from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

class PainQuestionnaireLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.selected_options = {}

        self.questions = [
            ("1. Pain Duration", self.show_pain_duration_options),
            ("2. Pain Perception", self.show_pain_perception_options),
            ("3. Pain Attacks", self.show_pain_attacks_options),
            ("4. Pain Sensation", self.show_pain_sensation_options),
            ("5. Area of Pain Descriptions", self.show_area_of_pain_options),
            ("6. Pain Profile", self.show_pain_profile_options),
        ]

        for question, func in self.questions:
            btn = Button(text=question, on_press=func, font_size="8mm")
            self.add_widget(btn)

        self.submit_button = Button(text='Submit', on_press=self.submit, background_color=(0, 1, 0, 1), font_size="8mm")
        self.add_widget(self.submit_button)

        self.add_widget(Button(text='Back', on_press=self.submit, background_color=(1, 0, 0, 1), font_size="8mm"))

    def show_options(self, title, options, task_name):
        dropdown = DropDown()
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=44, font_size="8mm")
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        spinner = Spinner(text='Select an option', values=options, size_hint=(1, 0.5), font_size="8mm")
        spinner.bind(text=lambda spinner, text: self.on_spinner_select(text, task_name))

        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(Label(text=title, font_size="8mm"))
        popup_layout.add_widget(spinner)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.5))
        popup.open()

    def on_spinner_select(self, text, task_name):
        self.selected_options[task_name] = text

    def show_pain_duration_options(self, instance):
        options = [
            '1. Less than 1 month', 
            '2. 1 month to 1/2 year', 
            '3. 1/2 year to 1 year', 
            '4. 1 to 2 years', 
            '5. 2 to 5 years', 
            '6. More than 5 years'
        ]
        self.show_options('Pain Duration', options, 'Pain Duration')

    def show_pain_perception_options(self, instance):
        options = [
            '1. Persistent pain with light fluctuations', 
            '2. Persistent pain with severe fluctuations', 
            '3. Pain attacks without pain in between', 
            '4. Pain attacks with pain in between'
        ]
        self.show_options('Pain Perception', options, 'Pain Perception')

    def show_pain_attacks_options(self, instance):
        sub_questions = [
            ("3a. Average Frequency", self.show_pain_attacks_frequency_options),
            ("3b. Average Duration", self.show_pain_attacks_duration_options),
            ("3c. Severe Pain at Certain Daytime", self.show_pain_attacks_daytime_options)
        ]
        self.show_subquestions('Pain Attacks', sub_questions)

    def show_pain_attacks_frequency_options(self, instance):
        options = [
            '1. Several times a day', 
            '2. Daily', 
            '3. Several times a week', 
            '4. Weekly', 
            '5. Several times a month', 
            '6. Monthly', 
            '7. Less often'
        ]
        self.show_options('Average Frequency', options, 'Pain Attacks Frequency')

    def show_pain_attacks_duration_options(self, instance):
        options = [
            '1. Seconds', 
            '2. Minutes', 
            '3. Hours', 
            '4. Up to 3 days', 
            '5. Longer than 3 days'
        ]
        self.show_options('Average Duration', options, 'Pain Attacks Duration')

    def show_pain_attacks_daytime_options(self, instance):
        options = [
            '1. No', 
            '2. Yes, in the morning', 
            '3. Yes, at noon', 
            '4. Yes, in the afternoon', 
            '5. Yes, in the evening', 
            '6. Yes, at night'
        ]
        self.show_options('Severe Pain at Certain Daytime', options, 'Pain Attacks Daytime')

    def show_pain_sensation_options(self, instance):
        sub_questions = [
            ("4a. Physical Pain Qualities", self.show_physical_pain_qualities_options),
            ("4b. Mental Pain Qualities", self.show_mental_pain_qualities_options)
        ]
        self.show_subquestions('Pain Sensation', sub_questions)

    def show_physical_pain_qualities_options(self, instance):
        options = [
            '1. Dull', 
            '2. Oppressive', 
            '3. Palpitant', 
            '4. Pulsating', 
            '5. Sharp', 
            '6. Dragging', 
            '7. Hot', 
            '8. Burning'
        ]
        self.show_options('Physical Pain Qualities', options, 'Physical Pain Qualities')

    def show_mental_pain_qualities_options(self, instance):
        options = [
            '1. Miserable', 
            '2. Dreadful', 
            '3. Excruciating', 
            '4. Terrible'
        ]
        self.show_options('Mental Pain Qualities', options, 'Mental Pain Qualities')

    def show_area_of_pain_options(self, instance):
        sub_questions = [
            ("5a. Burning Sensation", self.show_burning_sensation_options),
            ("5b. Formication", self.show_formication_options),
            ("5c. Light Touch is Painful", self.show_light_touch_painful_options),
            ("5d. Fulgurant, Electrifying Attacks", self.show_fulgurant_electrifying_attacks_options),
            ("5e. Sensitivity to Heat or Cold", self.show_sensitivity_to_heat_or_cold_options),
            ("5f. Numbness", self.show_numbness_options),
            ("5g. Light Push Painful", self.show_light_push_painful_options),
        ]
        self.show_subquestions('Area of Pain Descriptions', sub_questions)

    def show_burning_sensation_options(self, instance):
        options = [
            '1. Medium to high intensity', 
            '2. Never to low intensity'
        ]
        self.show_options('Burning Sensation', options, 'Burning Sensation')

    def show_formication_options(self, instance):
        options = [
            '1. Medium to high intensity', 
            '2. Never to low intensity'
        ]
        self.show_options('Formication', options, 'Formication')

    def show_light_touch_painful_options(self, instance):
        options = [
            '1. Medium to high intensity', 
            '2. Never to low intensity'
        ]
        self.show_options('Light Touch is Painful', options, 'Light Touch is Painful')

    def show_fulgurant_electrifying_attacks_options(self, instance):
        options = [
            '1. Medium to high intensity', 
            '2. Never to low intensity'
        ]
        self.show_options('Fulgurant, Electrifying Attacks', options, 'Fulgurant, Electrifying Attacks')

    def show_sensitivity_to_heat_or_cold_options(self, instance):
        options = [
            '1. Medium to high intensity', 
            '2. Never to low intensity'
        ]
        self.show_options('Sensitivity to Heat or Cold', options, 'Sensitivity to Heat or Cold')

    def show_numbness_options(self, instance):
        options = [
            '1. Medium to high intensity', 
            '2. Never to low intensity'
        ]
        self.show_options('Numbness', options, 'Numbness')

    def show_light_push_painful_options(self, instance):
        options = [
            '1. Medium to high intensity', 
            '2. Never to low intensity'
        ]
        self.show_options('Light Push Painful', options, 'Light Push Painful')

    def show_pain_profile_options(self, instance):
        options = [
            '1. Dorsal and plantar side of the feet',
            '2. Palmar side of the fingertips',
            '3. Dorsal side of the left palm',
            '4. Lower legs',
            '5. Vertebral column with the neck and tailbone, knee joints',
            '6. Shoulder region, elbows, thumb saddle joint',
            '7. Umbilical region, groin region, dorsal side of the knee joints, ankle joint, hand and finger joints, metatarsophalangeal joint, heel',
            '8. Parts of the ventral side of the thorax, lower side of the head'
        ]
        self.show_options('Pain Profile', options, 'Pain Profile')

    def show_subquestions(self, title, sub_questions):
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(Label(text=title, font_size="8mm"))
        for sub_question, func in sub_questions:
            btn = Button(text=sub_question, on_press=func, size_hint = (1, 0.5), font_size="8mm")
            popup_layout.add_widget(btn)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.8))
        popup.open()

    def submit(self, instance):
        print("Selected Options:")
        for task, option in self.selected_options.items():
            print(f"{task}: {option}")


class QuestionaireInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(QuestionaireInfoScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size)

        Window.bind(size=self.update_rect)

        self.add_widget(PainQuestionnaireLayout())

    def update_rect(self, *args):
        self.rect.size = Window.size


class PainQuestionnaireApp(App):
    def build(self):
        return PainQuestionnaireLayout()

if __name__ == '__main__':
    PainQuestionnaireApp().run()
