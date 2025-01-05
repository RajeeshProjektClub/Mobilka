from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, padding=10)
        self.solution = TextInput(background_color="black", foreground_color="white")
        
        # List of buttons with their associated screens
        buttons = [
            ("New Routine", "newRoutine"),
            ("Edit Routine", "editRoutine"),
            ("Get News", "news"),
            ("Bonus", "bonus")
        ]

        for label, screen in buttons:  # Unpack each button and its screen
            button = Button(
                text=label,
                font_size=30,
                background_color="grey",
                background_normal='',
                size_hint=(1, 1)  # Make button fill its cell in grid            
            )
            # Bind button to change screen
            button.bind(on_press=lambda x, s=screen: setattr(self.manager, 'current', s))
            layout.add_widget(button)

        self.add_widget(layout)

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        back_button = Button(text="Back to Home Screen")
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)

class MainApp(App):
    def build(self):
        self.icon = "superidol.png"
        sm = ScreenManager()

        # Add screens to the ScreenManager
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(SecondScreen(name="newRoutine"))
        sm.add_widget(SecondScreen(name="editRoutine"))
        sm.add_widget(SecondScreen(name="news"))
        sm.add_widget(SecondScreen(name="bonus"))

        return sm

if __name__ == "__main__":
    app = MainApp()
    app.run()
