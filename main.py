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
        
        buttons = [
            ("New Routine", "newRoutine"),
            ("Edit Routine", "editRoutine"),
            ("Get News", "news"),
            ("Bonus", "bonus")
        ]

        for label, screen in buttons:
            button = Button(
                text=label,
                font_size=30,
                background_color="grey",
                background_normal='',
                size_hint=(1, 1) 
            )
            button.bind(on_press=lambda x, s=screen: setattr(self.manager, 'current', s))
            layout.add_widget(button)

        self.add_widget(layout)


class NewRoutineScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Input fields for exercise name and repetitions
        self.name_input = TextInput(hint_text="Enter exercise name", size_hint=(1, 0.2))
        self.reps_input = TextInput(hint_text="Enter number of repetitions", size_hint=(1, 0.2), input_filter='int')

        # Button to create the routine
        create_button = Button(text="Create Routine", size_hint=(1, 0.2), background_color="green")
        create_button.bind(on_press=self.create_routine)

        # Back button to home screen
        back_button = Button(text="Back to Home Screen", size_hint=(1, 0.2))
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))

        # Add widgets to the layout
        layout.add_widget(self.name_input)
        layout.add_widget(self.reps_input)
        layout.add_widget(create_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def create_routine(self, instance):
        """Funkcja tworząca nową rutynę."""
        name = self.name_input.text
        reps = self.reps_input.text

        # Validate input and create routine
        if name and reps.isdigit():
            # Przechodzimy do ekranu z potwierdzeniem rutyny
            self.manager.get_screen('routineConfirmed').display_routine(name, reps)

            # Przejdź do ekranu z potwierdzeniem rutyny
            self.manager.current = "routineConfirmed"

            # Clear the input fields
            self.name_input.text = ""
            self.reps_input.text = ""
        else:
            print("Please fill in all fields correctly.")


class RoutineConfirmedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Label for displaying the routine details
        self.routine_label = TextInput(font_size=30, background_color="black", foreground_color="white", readonly=True)
        layout.add_widget(self.routine_label)

        # Button to add a new exercise
        add_button = Button(text="Add New Exercise", size_hint=(1, 0.2), background_color="blue")
        add_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'newRoutine'))
        layout.add_widget(add_button)

        # Add back button to home screen
        back_button = Button(text="Back to Home Screen", size_hint=(1, 0.2))
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def display_routine(self, name, reps):
        """Wyświetla szczegóły rutyny na ekranie."""
        self.routine_label.text = f"Exercise: {name}\nRepetitions: {reps}"


class MainApp(App):
    def build(self):
        sm = ScreenManager()

        # Add screens to the ScreenManager
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(NewRoutineScreen(name="newRoutine"))
        sm.add_widget(RoutineConfirmedScreen(name="routineConfirmed"))

        return sm


if __name__ == "__main__":
    app = MainApp()
    app.run()
