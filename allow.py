from kivy.app import App
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        return Button(text='Click Me', font_size=24, background_color=(0, 0.7, 0, 1))

MyApp().run()
