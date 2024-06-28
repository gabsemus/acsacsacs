from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class UserListScreen(Screen):
    selected_domicilio = {}  # Armazenar os dados do domicílio selecionado

    def on_kv_post(self, base_widget):
        self.user_list_grid = self.ids.user_list_grid

    def update_user_list(self, users):
        self.user_list_grid.clear_widgets()
        for user in users:
            user_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
            checkbox = CheckBox(size_hint_x=None, width='40dp', height='40dp')
            user_label = Label(
                text=user,
                size_hint_y=None,
                height='40dp',
                color=(0, 0, 0, 1),  # Set text color to black
                font_size='20sp'  # Increase font size for better visibility
            )
            user_layout.add_widget(checkbox)
            user_layout.add_widget(user_label)
            self.user_list_grid.add_widget(user_layout)

        # Add "Incluir Usuário" button
        include_user_button = Button(
            text='Incluir Usuário',
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            on_press=self.go_to_add_user
        )
        self.user_list_grid.add_widget(include_user_button)

    def on_back(self):
        self.manager.current = 'pomodoro'

    def on_confirm(self):
        selected_users = []
        for child in self.user_list_grid.children:
            if isinstance(child, BoxLayout):
                for subchild in child.children:
                    if isinstance(subchild, CheckBox) and subchild.active:
                        user_label = next((c for c in child.children if isinstance(c, Label)), None)
                        if user_label:
                            selected_users.append(user_label.text)
        if selected_users:
            self.manager.get_screen('user_details').set_user_details(selected_users)
            self.manager.current = 'user_details'

    def go_to_add_user(self, instance):
        if self.selected_domicilio:
            user_add_screen = self.manager.get_screen('user_add')
            user_add_screen.set_domicilio_data(self.selected_domicilio)
            self.manager.current = 'user_add'
