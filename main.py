# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from app.screens.pomodoro_screen import PomodoroForm
from app.screens.user_list_screen import UserListScreen
from app.screens.user_details_screen import UserDetailsScreen
from app.screens.user_add_screen import UserAddScreen
from app.screens.pending_screen import PendingScreen

class HomeScreen(Screen):
    pass

class PomodoroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(PomodoroForm())

class PomoDuno(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(PomodoroScreen(name='pomodoro'))
        sm.add_widget(UserListScreen(name='user_list'))
        sm.add_widget(UserAddScreen(name='user_add'))
        sm.add_widget(UserDetailsScreen(name='user_details'))
        sm.add_widget(PendingScreen(name='pending_screen'))
        return sm

if __name__ == '__main__':
    Builder.load_file('app/pomodoro.kv')
    Builder.load_file('app/home_screen.kv')
    Builder.load_file('app/pending_screen.kv')

    PomoDuno().run()
