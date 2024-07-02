from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from pain2d_info.main_pain2d import Pain2D_draw
from patient_info.main_patient import PatientInfoScreen
from questionaire_info.main_questionaire import QuestionaireInfoScreen


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=min(Window.size) * 0.15, padding=min(Window.size) * 0.3)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size)

        Window.bind(size=self.update_rect)

        btn_new = Button(text="New", font_size="12mm")
        btn_import = Button(text="Import", font_size="12mm")

        btn_new.bind(on_press=self.on_new_pressed)

        layout.add_widget(btn_new)
        layout.add_widget(btn_import)

        self.add_widget(layout)

    def update_rect(self):
        self.rect.size = Window.size

    def on_new_pressed(self, instance):
        self.manager.current = 'new_canvas'


class NewCanvasScreen(Screen):
    def __init__(self, **kwargs):
        super(NewCanvasScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=min(Window.size) * 0.05, padding=min(Window.size) * 0.1)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=Window.size)

        Window.bind(size=self.update_rect)

        btn1 = Button(text="Patient Info", font_size="12mm", color=(1, 1, 1, 1))
        btn2 = Button(text="Questionaire Info", font_size="12mm", color=(1, 1, 1, 1))
        btn3 = Button(text="Laboratory Info", font_size="12mm", color=(1, 1, 1, 1))
        btn4 = Button(text="Pain2D Info", font_size="12mm", color=(1, 1, 1, 1))
        btn5 = Button(text="Back", font_size="12mm", color=(1, 1, 1, 1))


        btn1.bind(on_press=self.run_patient_info)
        btn2.bind(on_press=self.run_questionaire_info)
        btn4.bind(on_press=self.run_pain2d)

        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        layout.add_widget(btn4)
        layout.add_widget(btn5)

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = Window.size

    def run_pain2d(self, instance):
        self.manager.current = 'pain2d'

    def run_patient_info(self, instance):
        self.manager.current = 'patient_info'

    def run_questionaire_info(self, instance):
        self.manager.current = 'questionaire_info'


class Pain2D(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(NewCanvasScreen(name='new_canvas'))
        sm.add_widget(Pain2D_draw(name='pain2d'))
        sm.add_widget(PatientInfoScreen(name='patient_info'))
        sm.add_widget(QuestionaireInfoScreen(name='questionaire_info'))
        return sm


if __name__ == '__main__':
    Pain2D().run()
