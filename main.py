import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Rectangle


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=0, padding=0)

        # Add canvas for background color (split into top and bottom sections)
        with self.canvas.before:
            # Szary kolor na 4/5 wysokości
            Color(0.1, 0.1, 0.1, 1)  # Ciemnoszary kolor tła
            self.rect_top = Rectangle(size=(self.width, self.height * 0.8), pos=(0, self.height * 0.2))

            # Niebieski kolor na 1/5 wysokości (teraz jaśniejszy niebieski)
            Color(0.6, 0.8, 1, 1)  # Bardzo jasny niebieski kolor tła
            self.rect_bottom = Rectangle(size=(self.width, self.height * 0.2), pos=(0, 0))

        # Górna część layoutu (niezajmująca miejsca w dolnej sekcji)
        self.top_layout = BoxLayout(size_hint=(1, 0.8))  # Górna część
        layout.add_widget(self.top_layout)

        # Dolna część layoutu z przyciskami
        self.bottom_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))  # Dolna część
        nav_layout = GridLayout(cols=5, size_hint=(1, 1), spacing=20, padding=10)

        buttons = [
            ("New Routine", "newRoutine", "new_routine.png"),
            ("Edit Routine", "editRoutine", "edit_routine.png"),
            ("Get News", "news", "get_news.png"),
            ("Bonus", "bonus", "bonus.png"),
            ("Saved Plan", "savedPlan", "saved_plan.png")
        ]

        for label, screen, icon in buttons:
            button_layout = BoxLayout(orientation="vertical", size_hint=(1, 1))
            icon_widget = Image(source=icon, size_hint=(1, 0.3))
            text_widget = Button(
                text=label,
                size_hint=(1, 0.3),
                font_size=12,
                background_normal='',
                background_color=(1, 1, 1, 0),  # Customize color as needed
                color=(0.1, 0.4, 0.8, 1),
            )
            text_widget.bind(on_press=lambda x, s=screen: setattr(self.manager, 'current', s))
            button_layout.add_widget(icon_widget)
            button_layout.add_widget(text_widget)
            nav_layout.add_widget(button_layout)

        self.bottom_layout.add_widget(nav_layout)
        layout.add_widget(self.bottom_layout)

        self.add_widget(layout)

    def on_size(self, *args):
        """Update the background size when the screen size changes."""
        self.rect_top.pos = (0, self.height * 0.2)
        self.rect_top.size = (self.width, self.height * 0.8)

        self.rect_bottom.pos = (0, 0)
        self.rect_bottom.size = (self.width, self.height * 0.2)


class NewRoutineScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=5, padding=10)

        # Add canvas for background color (dark gray or near black)
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Ciemnoszary kolor tła
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Input fields for exercise name and repetitions
        self.name_input = TextInput(hint_text="Enter exercise name", size_hint=(1, 0.2))
        self.reps_input = TextInput(hint_text="Enter number of repetitions", size_hint=(1, 0.2), input_filter='int')

        # Button to create the routine
        create_button = Button(text="Create Routine", size_hint=(1, 0.2), background_color=(0, 0.639, 0.545, 1))
        create_button.bind(on_press=self.create_routine)

        # Back button to home screen
        back_button = Button(text="Back to Home Screen", size_hint=(1, 0.2), background_color=(1, 0.322, 0.133, 1))
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))

        # Add widgets to the layout
        layout.add_widget(self.name_input)
        layout.add_widget(self.reps_input)
        layout.add_widget(create_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_size(self, *args):
        """Update the background size when the screen size changes."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def create_routine(self, instance):
        """Create a new routine."""
        name = self.name_input.text
        reps = self.reps_input.text

        if name and reps.isdigit():
            # Prepare JSON data
            routine_data = {
                "exercise_name": name,
                "repetitions": int(reps)
            }
            self.export_to_json(routine_data)

            # Clear input fields and navigate
            self.manager.current = "home"
            self.name_input.text = ""
            self.reps_input.text = ""
        else:
            print("Please fill in all fields correctly.")

    def export_to_json(self, data):
        """Export routine to JSON and print to console."""
        json_output = json.dumps(data, indent=4)
        print(f"Routine JSON output:\n{json_output}")


class RoutineConfirmedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=5, padding=10)

        # Add canvas for background color (dark gray or near black)
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Ciemnoszary kolor tła
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Placeholder routine confirmation content
        routine_label = TextInput(
            font_size=20,
            text="Routine confirmed! Add more features here.",
            readonly=True
        )
        layout.add_widget(routine_label)

        # Back button to home screen
        back_button = Button(text="Back to Home Screen", size_hint=(1, 0.2), background_color=(1, 0.322, 0.133, 1))
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_size(self, *args):
        """Update the background size when the screen size changes."""
        self.rect.pos = self.pos
        self.rect.size = self.size


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
