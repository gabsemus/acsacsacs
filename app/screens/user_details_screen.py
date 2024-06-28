from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
import pandas as pd
from datetime import datetime

class UserDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_index = 0
        self.user_details = []
        self.data = pd.read_csv('app/ACS.csv', dtype=str)
        self.desvincular_checkbox = None
        self.registrar_visita_checkbox = None
        self.atualizar_cadastro_checkbox = None  # New checkbox for updating user

    def set_user_details(self, users):
        self.user_details = users
        self.current_index = 0
        self.display_user_details()

    def display_user_details(self):
        self.ids.user_details_grid.clear_widgets()
        if self.user_details:
            user = self.user_details[self.current_index]
            user_data_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='150dp')
            for detail in user.split(', '):
                user_data_layout.add_widget(Label(
                    text=detail,
                    size_hint_y=None,
                    height='30dp',
                    color=(0, 0, 0, 1),
                    font_size='20sp'
                ))
            self.ids.user_details_grid.add_widget(user_data_layout)

            # Add some spacing between user details and actions
            self.ids.user_details_grid.add_widget(BoxLayout(size_hint_y=None, height='20dp'))

            # Add actions section
            actions_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='180dp')
            actions_label = Label(
                text='Ações',
                size_hint_y=None,
                height='30dp',
                color=(0.2, 0.6, 0.86, 1),
                font_size='20sp'
            )
            actions_layout.add_widget(actions_label)

            # Add desvincular option
            desvincular_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
            desvincular_label = Label(
                text='Desvincular Usuário',
                size_hint_x=0.7,
                color=(0, 0, 0, 1),
                font_size='18sp'
            )
            self.desvincular_checkbox = CheckBox(size_hint_x=0.3)
            desvincular_layout.add_widget(desvincular_label)
            desvincular_layout.add_widget(self.desvincular_checkbox)
            actions_layout.add_widget(desvincular_layout)

            # Add registrar visita option
            registrar_visita_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
            registrar_visita_label = Label(
                text='Registrar Visita',
                size_hint_x=0.7,
                color=(0, 0, 0, 1),
                font_size='18sp'
            )
            self.registrar_visita_checkbox = CheckBox(size_hint_x=0.3)
            registrar_visita_layout.add_widget(registrar_visita_label)
            registrar_visita_layout.add_widget(self.registrar_visita_checkbox)
            actions_layout.add_widget(registrar_visita_layout)

            # Add atualizar cadastro option
            atualizar_cadastro_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
            atualizar_cadastro_label = Label(
                text='Atualizar Cadastro',
                size_hint_x=0.7,
                color=(0, 0, 0, 1),
                font_size='18sp'
            )
            self.atualizar_cadastro_checkbox = CheckBox(size_hint_x=0.3)
            atualizar_cadastro_layout.add_widget(atualizar_cadastro_label)
            atualizar_cadastro_layout.add_widget(self.atualizar_cadastro_checkbox)
            actions_layout.add_widget(atualizar_cadastro_layout)

            self.ids.user_details_grid.add_widget(actions_layout)

            # Add save button
            save_button = Button(
                text='Salvar',
                size_hint_y=None,
                height='30dp',
                background_color=(0.2, 0.6, 0.86, 1),
                color=(1, 1, 1, 1)
            )
            save_button.bind(on_press=self.save_changes)
            self.ids.user_details_grid.add_widget(save_button)

    def save_changes(self, instance):
        user = self.user_details[self.current_index]
        user_id = user.split(': ')[0]

        # Read the CSV file again to ensure it is up to date
        self.data = pd.read_csv('app/ACS.csv', dtype=str)

        if self.desvincular_checkbox.active:
            # Update the fields for the specific user
            self.data.loc[self.data['CODIGO_PRONTO'] == user_id,
                          ['ID', 'SEGMENTO', 'AREA', 'MICRO_AREA', 'CODIGO', 'CEP', 'NUMERO', 'COMPLEMENTO', 'STATUS',
                           'RUA', 'BAIRRO']] = ''

        if self.registrar_visita_checkbox.active:
            # Update the DATA field for the specific user
            today_date = datetime.now().strftime('%d/%m/%Y')
            self.data.loc[self.data['CODIGO_PRONTO'] == user_id, 'DATA'] = today_date

        if self.atualizar_cadastro_checkbox.active:
            # Add logic to update user details as needed
            print(f"Updating user {user_id}'s details")

        # Save the updated DataFrame back to the CSV
        self.data.to_csv('app/ACS.csv', index=False)
        print(f"User {user_id} updated and changes saved to CSV.")

        # Update local user details to reflect the changes
        self.user_details[self.current_index] = self.data[self.data['CODIGO_PRONTO'] == user_id].to_dict('records')[0]

        self.manager.current = 'user_list'

    def next_page(self):
        if self.current_index < len(self.user_details) - 1:
            self.current_index += 1
            self.display_user_details()

    def prev_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_user_details()

    def on_back(self):
        self.manager.current = 'user_list'
