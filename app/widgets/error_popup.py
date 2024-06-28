from kivy.uix.popup import Popup
from kivy.uix.label import Label

class ErrorPopup(Popup):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Error'
        self.size_hint = (None, None)
        self.size = (400, 200)
        self.content = Label(text=message)
