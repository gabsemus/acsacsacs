from kivy.uix.spinner import SpinnerOption

class CustomSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0.96, 0.96, 0.96, 1)  # Off-white background
        self.color = (0.2, 0.6, 0.86, 1)  # Blue text color
