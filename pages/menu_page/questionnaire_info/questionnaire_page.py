from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from ...base_page.base_page import BasePage

from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup


class QuestionnairePage(BasePage):
    def __init__(self, **kwargs):
        super(QuestionnairePage, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation="vertical")

        top_nested_layout = BoxLayout(orientation="vertical")

        self.selected_options = {}

        self.questions = [
            ("1. Pain Duration", self.show_pain_duration_options),
            ("2. Pain Perception", self.show_pain_perception_options),
            ("3. Pain Attacks", self.show_pain_attacks_options),
            ("4. Pain Sensation", self.show_pain_sensation_options),
            ("5. Area of Pain Descriptions", self.show_area_of_pain_options),
        ]

        for question, func in self.questions:
            btn = Button(text=question, on_press=func)
            top_nested_layout.add_widget(btn)

        bottom_nested_layout = BoxLayout(orientation="vertical")

        btn5 = Button(text="Submit", background_color=(0, 1, 0, 1))
        btn6 = Button(text="Back", background_color=(1, 0, 0, 1))

        btn6.bind(on_press=self.go_back)

        bottom_nested_layout.add_widget(btn5)
        bottom_nested_layout.add_widget(btn6)

        # Set the size_hint for the nested layouts before adding them
        top_nested_layout.size_hint = (1, 0.9)
        bottom_nested_layout.size_hint = (1, 0.1)

        # Add both nested layouts to the main layout
        main_layout.add_widget(top_nested_layout)
        main_layout.add_widget(bottom_nested_layout)

        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.current = 'menu_page'

    def show_options(self, title, options, task_name):
        spinner = Spinner(text='Select an option', values=options, size_hint=(1, 0.5), font_size="8mm")
        spinner.bind(text=lambda spinner, text: self.on_spinner_select(text, task_name))

        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(Label(text=title, font_size="8mm"))
        popup_layout.add_widget(spinner)

        # Adding Back Button to the Popup
        popup_layout.add_widget(
            Button(text='Back', size_hint=(1, 0.5), font_size="8mm", on_press=lambda btn: popup.dismiss()))

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

    def show_subquestions(self, title, sub_questions):
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(Label(text=title, font_size="8mm"))
        for sub_question, func in sub_questions:
            btn = Button(text=sub_question, on_press=func, size_hint=(1, 0.5), font_size="8mm")
            popup_layout.add_widget(btn)

        # Adding Back Button to the Subquestions Popup
        popup_layout.add_widget(
            Button(text='Back', size_hint=(1, 0.5), font_size="8mm", on_press=lambda btn: popup.dismiss()))

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.8))
        popup.open()


class MyApp(App):
    def build(self):
        return QuestionnairePage()


if __name__ == "__main__":
    MyApp().run()