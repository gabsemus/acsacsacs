import pandas as pd
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import datetime

class UserAddScreen(Screen):
    domicilio_data = {}  # Armazenar os dados do domicílio selecionado
    user_data = None  # Armazenar os dados do usuário encontrado

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')

        # Texto acima do campo de busca
        search_label = Label(
            text='Digite o Número do CPF do Usuário',
            font_size='20sp',
            size_hint_y=None,
            height='40dp',
            color=(0.2, 0.6, 0.86, 1)
        )

        # Sub-layout para o campo de busca e botão "Buscar"
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        self.text_input = TextInput(
            multiline=False,
            input_filter='int',
            font_size='20sp',
            size_hint_x=0.7,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        search_button = Button(
            text='Buscar',
            size_hint_x=0.3,
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            on_press=self.search_user
        )
        search_layout.add_widget(self.text_input)
        search_layout.add_widget(search_button)

        # Sub-layout para os dados do usuário
        self.user_info_box = BoxLayout(orientation='vertical', padding='10dp', spacing='15dp', size_hint_y=None)

        # Espaço entre o campo de busca e os dados do usuário
        self.space_widget = BoxLayout(size_hint_y=None, height='150dp')

        # Sub-layout para o botão "Adicionar"
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='50dp', spacing='10dp')
        self.add_button = Button(
            text='Adicionar',
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            on_press=self.add_user,
            disabled=True  # Inicialmente desativado
        )
        button_layout.add_widget(self.add_button)

        # Adicionar sub-layouts ao layout principal
        self.layout.add_widget(search_label)
        self.layout.add_widget(search_layout)
        self.layout.add_widget(self.space_widget)
        self.layout.add_widget(self.user_info_box)
        self.layout.add_widget(button_layout)

        self.add_widget(self.layout)

    def set_domicilio_data(self, data):
        self.domicilio_data = data

    def add_user(self, instance):
        if self.user_data is None:
            self.show_error_popup("Realize a busca do usuário antes de salvar.")
            return

        numero_usuario = self.text_input.text
        if len(numero_usuario) != 11:
            self.show_error_popup("O número deve ter 11 dígitos.")
        else:
            # Adicionar nova linha no DataFrame e salvar
            self.add_new_user()
            self.manager.current = 'user_list'
            self.text_input.text = ""  # Limpar o campo de entrada

    def search_user(self, instance):
        numero_usuario = self.text_input.text
        if len(numero_usuario) != 11:
            self.show_error_popup("O número deve ter 11 dígitos.")
            return

        try:
            df = pd.read_csv('app/USUARIO.csv', dtype=str, encoding='latin1')
            user_data = df[df['REPLACE_USUARIOCPF'] == numero_usuario]

            if user_data.empty:
                self.show_error_popup("Usuário não encontrado.")
            else:
                self.user_data = user_data.iloc[0]
                self.display_user_info(self.user_data)
                self.add_button.disabled = False  # Ativar o botão "Adicionar"
        except UnicodeDecodeError:
            self.show_error_popup("Erro ao ler o arquivo CSV. Verifique a codificação do arquivo.")

    def display_user_info(self, user_info):
        self.user_info_box.clear_widgets()
        user_info_labels = [
            f"Nome: {user_info['USUARIONOME']}",
            f"Data de Nascimento: {user_info['DATA_NASCIMENTO']}",
            f"Sexo: {user_info['SEXO']}",
            f"CPF: {user_info['USUARIOCPF']}",
            f"CNS: {user_info['USUARIONUMEROCNS']}",
            f"Data de Alteração: {user_info['USUARIODATAALTERACAO']}",
            f"Status: {user_info['STATUS']}"
        ]
        for info in user_info_labels:
            label = Label(text=info, font_size='20sp', color=(0, 0, 0, 1), halign='left', valign='middle', size_hint_y=None, height='20dp')
            label.bind(size=self._update_text_width)
            self.user_info_box.add_widget(label)

    def _update_text_width(self, instance, value):
        instance.text_size = (instance.width, None)

    def show_error_popup(self, message):
        popup_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        popup_label = Label(text=message, font_size='18sp', size_hint_y=None, height='50dp', color=(1, 0, 0, 1))
        popup_button = Button(
            text='Fechar',
            size_hint_y=None,
            height='50dp',
            on_press=lambda x: self.popup.dismiss()
        )
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        self.popup = Popup(
            title='Erro',
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )
        self.popup.open()

    def add_new_user(self):
        # Carregar o DataFrame existente
        df = pd.read_csv('app/ACS.csv', dtype=str)

        # Verificar se já existe uma linha com o mesmo USUARIOID e removê-la
        df = df[df['CODIGO_PRONTO'] != self.user_data['USUARIOID']]

        # Adicionar nova linha com dados do domicílio e colunas especificadas
        new_row = {
            'ID': self.domicilio_data.get('ID', ''),
            'SEGMENTO': self.domicilio_data.get('SEGMENTO', ''),
            'AREA': self.domicilio_data.get('AREA', ''),
            'MICRO_AREA': self.domicilio_data.get('MICRO_AREA', ''),
            'CODIGO': self.domicilio_data.get('CODIGO', ''),
            'CEP': self.domicilio_data.get('CEP', ''),
            'NUMERO': self.domicilio_data.get('NUMERO', ''),
            'COMPLEMENTO': self.domicilio_data.get('COMPLEMENTO', ''),
            'STATUS': self.domicilio_data.get('STATUS', ''),
            'RUA': self.domicilio_data.get('RUA', ''),
            'BAIRRO': self.domicilio_data.get('BAIRRO', ''),
            'INDIVIDUALNOME': self.user_data['USUARIONOME'],
            'CODIGO_PRONTO': self.user_data['USUARIOID'],
            'DATA': datetime.today().strftime('%d/%m/%Y')
        }

        # Convert new_row to DataFrame
        new_row_df = pd.DataFrame([new_row])

        # Concatenate the new row to the existing DataFrame
        df = pd.concat([df, new_row_df], ignore_index=True)

        # Salvar o DataFrame atualizado de volta ao arquivo CSV
        df.to_csv('app/ACS.csv', index=False)

        print(f'Domicílio adicionado com número: {self.domicilio_data.get("NUMERO", "")}')
