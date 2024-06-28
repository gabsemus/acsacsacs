import time
import threading
import pandas as pd
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, NumericProperty
from kivy.clock import mainthread
from app.widgets.custom_spinner_option import CustomSpinnerOption
from app.widgets.error_popup import ErrorPopup

class PomodoroForm(BoxLayout):
    segmento_list = ListProperty([])
    area_list = ListProperty([])
    micro_area_list = ListProperty([])
    numero_list = ListProperty([])
    complemento_list = ListProperty([])
    rua_list = ListProperty([])
    bairro_list = ListProperty([])
    filtered_data = None
    current_index = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segmento_list = ['']
        self.area_list = ['']
        self.micro_area_list = ['']
        self.numero_list = ['']
        self.complemento_list = ['']
        self.rua_list = ['']
        self.bairro_list = ['']
        threading.Thread(target=self.load_bairro_data).start()

    @mainthread
    def show_error(self, message):
        error_popup = ErrorPopup(message)
        error_popup.open()

    def load_bairro_data(self):
        try:
            start_time = time.time()
            self.data = pd.read_csv('app/ACS.csv', dtype=str)
            read_time = time.time()
            print(f"Time to read the CSV file: {read_time - start_time} seconds")
            bairro_list = list(self.data['BAIRRO'].dropna().unique().astype(str))
            bairro_list.insert(0, 'Selecione o BAIRRO')
            processing_time = time.time()
            print(f"Time to process BAIRRO data: {processing_time - read_time} seconds")
            self.update_bairro_list(bairro_list)
            bairro_df = pd.DataFrame(bairro_list[1:], columns=['BAIRRO'])
            bairro_df.to_csv('app/unique_bairro.csv', index=False)
            save_time = time.time()
            print(f"Time to save unique BAIRRO values: {save_time - processing_time} seconds")
        except Exception as e:
            self.show_error(str(e))

    @mainthread
    def update_bairro_list(self, bairro_list):
        self.bairro_list = bairro_list

    def update_rua_spinner(self):
        try:
            self.data = pd.read_csv('app/ACS.csv', dtype=str)  # Reload the CSV
            selected_bairro = self.ids.bairro_spinner.text
            if selected_bairro != 'Selecione o BAIRRO':
                filtered_data = self.data[self.data['BAIRRO'] == selected_bairro]
                rua_list = list(filtered_data['RUA'].dropna().unique().astype(str))
                rua_list.insert(0, 'Selecione a RUA')
                self.rua_list = rua_list
                rua_df = pd.DataFrame(rua_list[1:], columns=['RUA'])
                rua_df.to_csv('app/unique_rua.csv', index=False)
            else:
                self.rua_list = ['']
                self.numero_list = ['']
                self.complemento_list = ['']
        except Exception as e:
            self.show_error(str(e))

    def update_numero_spinner(self):
        try:
            self.data = pd.read_csv('app/ACS.csv', dtype=str)  # Reload the CSV
            selected_bairro = self.ids.bairro_spinner.text
            selected_rua = self.ids.rua_spinner.text
            if selected_rua != 'Selecione a RUA':
                filtered_data = self.data[(self.data['BAIRRO'] == selected_bairro) & (self.data['RUA'] == selected_rua)]
                numero_list = list(filtered_data['NUMERO'].dropna().unique().astype(str))
                numero_list.insert(0, 'Selecione o NUMERO')
                self.numero_list = numero_list
                numero_df = pd.DataFrame(numero_list[1:], columns=['NUMERO'])
                numero_df.to_csv('app/unique_numero.csv', index=False)
            else:
                self.numero_list = ['']
                self.complemento_list = ['']
        except Exception as e:
            self.show_error(str(e))

    def update_complemento_spinner(self):
        try:
            self.data = pd.read_csv('app/ACS.csv', dtype=str)  # Reload the CSV
            selected_bairro = self.ids.bairro_spinner.text
            selected_rua = self.ids.rua_spinner.text
            selected_numero = self.ids.numero_spinner.text
            if selected_numero != 'Selecione o NUMERO':
                filtered_data = self.data[
                    (self.data['BAIRRO'] == selected_bairro) &
                    (self.data['RUA'] == selected_rua) &
                    (self.data['NUMERO'] == selected_numero)
                ]
                complemento_list = list(filtered_data['COMPLEMENTO'].dropna().unique().astype(str))
                complemento_list.insert(0, 'Selecione o COMPLEMENTO')
                self.complemento_list = complemento_list
                complemento_df = pd.DataFrame(complemento_list[1:], columns=['COMPLEMENTO'])
                complemento_df.to_csv('app/unique_complemento.csv', index=False)
            else:
                self.complemento_list = ['']
        except Exception as e:
            self.show_error(str(e))

    def update_user_display(self):
        try:
            self.data = pd.read_csv('app/ACS.csv', dtype=str)  # Reload the CSV
            selected_bairro = self.ids.bairro_spinner.text
            selected_rua = self.ids.rua_spinner.text
            selected_numero = self.ids.numero_spinner.text
            selected_complemento = self.ids.complemento_spinner.text
            if selected_complemento != 'Selecione o COMPLEMENTO':
                self.filtered_data = self.data[
                    (self.data['BAIRRO'] == selected_bairro) &
                    (self.data['RUA'] == selected_rua) &
                    (self.data['NUMERO'] == selected_numero) &
                    (self.data['COMPLEMENTO'] == selected_complemento)
                ].sort_values(by='DATA')  # Sort by DATA field
                self.current_index = 0
                self.display_user()
            else:
                self.clear_fields()
        except Exception as e:
            self.show_error(str(e))

    @mainthread
    def display_user(self):
        if self.filtered_data is not None and not self.filtered_data.empty:
            row = self.filtered_data.iloc[self.current_index]
            self.ids.area_label.text = str(row['AREA'])
            self.ids.codigo_label.text = str(row['CODIGO'])
        else:
            self.clear_fields()

    def next_user(self):
        if self.filtered_data is not None and self.current_index < len(self.filtered_data) - 1:
            self.current_index += 1
            self.display_user()

    def prev_user(self):
        if self.filtered_data is not None and self.current_index > 0:
            self.current_index -= 1
            self.display_user()

    def load_data(self):
        try:
            self.display_user()
        except Exception as e:
            self.show_error(str(e))

    def clear_fields(self):
        self.ids.area_label.text = ''
        self.ids.codigo_label.text = ''

    def visualizar_residencia(self):
        if self.filtered_data is not None and not self.filtered_data.empty:
            users = self.filtered_data[['CODIGO_PRONTO', 'INDIVIDUALNOME']].dropna()
            user_list = [f"{row['CODIGO_PRONTO']}: {row['INDIVIDUALNOME']}" for index, row in users.iterrows()]
            self.parent.manager.current = 'user_list'
            user_list_screen = self.parent.manager.get_screen('user_list')
            user_list_screen.update_user_list(user_list)
            # Passar os dados do domicílio filtrado
            user_list_screen.selected_domicilio = self.filtered_data.iloc[0].to_dict()

    def go_to_home(self):
        self.parent.manager.current = 'home'
