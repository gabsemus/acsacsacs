# pending_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from kivy.uix.label import Label
import pandas as pd

class PendingScreen(Screen):
    area_list = ListProperty(['Selecione a AREA'])
    codigo_list = ListProperty(['Selecione o CODIGO'])
    selected_area = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_data()

    def load_data(self):
        try:
            self.data = pd.read_csv('app/acs.csv', dtype=str)
            self.area_list = ['Selecione a AREA'] + self.data['AREA'].dropna().unique().tolist()
        except Exception as e:
            print(f"Error loading data: {e}")

    def update_codigo_spinner(self):
        if self.ids.area_spinner.text and self.ids.area_spinner.text != 'Selecione a AREA':
            self.selected_area = self.ids.area_spinner.text
            filtered_data = self.data[self.data['AREA'] == self.selected_area]
            self.codigo_list = ['Selecione o CODIGO'] + filtered_data['CODIGO'].dropna().unique().tolist()
        else:
            self.codigo_list = ['Selecione o CODIGO']

    def search_pendencias(self):
        area = self.ids.area_spinner.text
        codigo = self.ids.codigo_spinner.text

        # Check if the filters are selected properly
        if area == 'Selecione a AREA' or codigo == 'Selecione o CODIGO':
            print("Selecione valores válidos para AREA e CODIGO")
            return

        filtered_data = self.data[
            (self.data['AREA'] == area) &
            (self.data['CODIGO'] == codigo)
        ].drop_duplicates(subset=['BAIRRO', 'RUA', 'NUMERO', 'COMPLEMENTO']).head(10)

        self.ids.grid_pendencias.clear_widgets()

        # Add header row
        header = ['BAIRRO', 'RUA', 'NUMERO', 'COMPLEMENTO']
        for col in header:
            self.ids.grid_pendencias.add_widget(Label(text=col, size_hint_y=None, height='30dp', color=(0, 0, 0, 1), bold=True))

        for index, row in filtered_data.iterrows():
            for col in header:
                self.ids.grid_pendencias.add_widget(Label(text=str(row[col]), size_hint_y=None, height='30dp', color=(0, 0, 0, 1)))
