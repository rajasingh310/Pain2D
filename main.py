from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from pages.base_page.base_page import FirstPage
from pages.menu_page.menu_page import MenuPage
#from pages.menu_page.patient_info.patient_page import PatientPage
#from pages.menu_page.questionnaire_info.questionnaire_page import QuestionnairePage
#from pages.menu_page.laboratory_info.laboratory_page import LaboratoryPage
from pages.menu_page.seepain_info.seepain_page import SeePainPage


class MyApp(App):
    def build(self):
        self.title = 'SeePain'  # Set the title here
        self.icon = "seepain_logo.png"
        sm = ScreenManager()
        sm.add_widget(FirstPage(name='first_page'))
        sm.add_widget(MenuPage(name='menu_page'))
        #sm.add_widget(PatientPage(name='patient_page'))
        #sm.add_widget(QuestionnairePage(name='questionnaire_page'))
        #sm.add_widget(LaboratoryPage(name='laboratory_page'))
        sm.add_widget(SeePainPage(name='seepain_page'))
        return sm


if __name__ == '__main__':
    MyApp().run()
