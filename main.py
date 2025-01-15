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

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark gray
            self.rect_top = Rectangle(size=(self.width, self.height * 0.8), pos=(0, self.height * 0.2))

            Color(0.6, 0.8, 1, 1)  # Light blue
            self.rect_bottom = Rectangle(size=(self.width, self.height * 0.2), pos=(0, 0))

        self.top_layout = BoxLayout(size_hint=(1, 0.8))
        layout.add_widget(self.top_layout)

        self.bottom_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
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
                background_color=(1, 1, 1, 0),
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
        self.rect_top.pos = (0, self.height * 0.2)
        self.rect_top.size = (self.width, self.height * 0.8)

        self.rect_bottom.pos = (0, 0)
        self.rect_bottom.size = (self.width, self.height * 0.2)


class NewRoutineScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=5, padding=10)

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.name_input = TextInput(hint_text="Enter exercise name", size_hint=(1, 0.2))
        self.reps_input = TextInput(hint_text="Enter number of repetitions", size_hint=(1, 0.2), input_filter='int')

        create_button = Button(text="Create Routine", size_hint=(1, 0.2), background_color=(0, 0.639, 0.545, 1))
        create_button.bind(on_press=self.create_routine)

        back_button = Button(text="Back to Home Screen", size_hint=(1, 0.2), background_color=(1, 0.322, 0.133, 1))
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))

        layout.add_widget(self.name_input)
        layout.add_widget(self.reps_input)
        layout.add_widget(create_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_size(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def create_routine(self, instance):
        name = self.name_input.text
        reps = self.reps_input.text

        if name and reps.isdigit():
            routine_data = {
                "exercise_name": name,
                "repetitions": int(reps)
            }
            self.manager.get_screen('routineConfirmed').add_exercise(name, reps)
            self.manager.current = "routineConfirmed"
            self.name_input.text = ""
            self.reps_input.text = ""
        else:
            print("Please fill in all fields correctly.")


class RoutineConfirmedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.routine_label = TextInput(
            font_size=20,
            text="Routine confirmed! Add more features here.",
            readonly=True
        )
        layout.add_widget(self.routine_label)

        add_button = Button(text="Add New Exercise", size_hint=(1, 0.2), background_color=(0, 0.482, 0.859, 1))
        add_button.bind(on_press=self.go_to_new_routine)
        layout.add_widget(add_button)

        save_button = Button(text="Save Plan", size_hint=(1, 0.2), background_color=(0.243, 0.318, 0.712, 1))
        save_button.bind(on_press=self.save_plan)
        layout.add_widget(save_button)

        back_button = Button(text="Back to Home Screen", size_hint=(1, 0.2), background_color=(1, 0.322, 0.133, 1))
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)
        self.exercises = []

    def add_exercise(self, name, reps):
        self.exercises.append({"exercise_name": name, "repetitions": reps})
        self.update_routine_display()

    def update_routine_display(self):
        display_text = "\n".join([f"Exercise: {e['exercise_name']}, Reps: {e['repetitions']}" for e in self.exercises])
        self.routine_label.text = display_text

    def go_to_new_routine(self, instance):
        self.manager.current = 'newRoutine'

    def save_plan(self, instance):
        if self.exercises:
            saved_plan = {"plan_name": "", "exercises": self.exercises}
            plan_name = input("Enter a name for your plan: ")  # Temporary solution for naming plans
            saved_plan["plan_name"] = plan_name

            self.manager.get_screen('savedPlan').add_saved_plan(saved_plan)
            self.exercises = []
            self.update_routine_display()


class SavedPlanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.plans_list = BoxLayout(orientation="vertical", spacing=10)
        layout.add_widget(self.plans_list)

        self.plan_details = TextInput(
            font_size=16,
            readonly=True,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            size_hint=(1, 0.7)
        )
        layout.add_widget(self.plan_details)

        back_button = Button(text="Back to Home Screen", size_hint=(1, 0.1), background_color=(1, 0.322, 0.133, 1))
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)
        self.saved_plans = []

    def add_saved_plan(self, plan):
        self.saved_plans.append(plan)
        self.update_saved_plans_display()

    def update_saved_plans_display(self):
        self.plans_list.clear_widgets()
        for i, plan in enumerate(self.saved_plans):
            plan_button = Button(
                text=f"{plan['plan_name']}",
                size_hint=(1, None),
                height=40,
                background_color=(0.243, 0.318, 0.712, 1)
            )
            plan_button.bind(on_press=lambda x, p=plan: self.show_plan_details(p))
            self.plans_list.add_widget(plan_button)

    def show_plan_details(self, plan):
        details = json.dumps(plan, indent=4)
        self.plan_details.text = details


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(NewRoutineScreen(name="newRoutine"))
        sm.add_widget(RoutineConfirmedScreen(name="routineConfirmed"))
        sm.add_widget(SavedPlanScreen(name="savedPlan"))

        return sm


if __name__ == "__main__":
    app = MainApp()
    app.run()
