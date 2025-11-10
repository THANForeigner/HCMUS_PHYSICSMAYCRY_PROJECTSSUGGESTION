import flet as ft
import time

def mock_auth_login(email, pwd):
    if email == "test@university.edu" and pwd == "123":
        return {"email": email, "name": "Test User"}
    return None

def mock_auth_register(email, pwd, name):
    if email == "new@university.edu":
        return None
    return {"email": email, "name": name}

class AuthForm(ft.Container):
    def __init__(self, on_auth_success):
        super().__init__(
            width=420,
            bgcolor=ft.Colors.WHITE,
            padding=0,
        )
        self.on_auth_success = on_auth_success

        self.login_email = ft.TextField(label="Email",text_style=ft.TextStyle(
            color=ft.Colors.BLACK
        ), hint_text="student@university.edu", on_change=self.hide_error)
        self.login_password = ft.TextField(label="Password",text_style=ft.TextStyle(
            color=ft.Colors.BLACK
        ), password=True, can_reveal_password=True, on_change=self.hide_error)
        self.register_name = ft.TextField(label="Full Name",text_style=ft.TextStyle(
            color=ft.Colors.BLACK
        ), hint_text="John Doe", on_change=self.hide_error)
        self.register_email = ft.TextField(label="Email", text_style=ft.TextStyle(
            color=ft.Colors.BLACK
        ),hint_text="student@university.edu", on_change=self.hide_error)
        self.register_password = ft.TextField(label="Password", text_style=ft.TextStyle(
            color=ft.Colors.BLACK
        ),password=True, can_reveal_password=True, on_change=self.hide_error)

        self.error_message = ft.Text("", color=ft.Colors.RED_500, visible=False, text_align=ft.TextAlign.CENTER)

        login_tab = ft.Container(
            content=ft.Column([
                self.login_email,
                self.login_password,
                ft.Container(height=10),
                ft.Row([
                    ft.FilledButton("Login", on_click=self.handle_login, expand=True,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=15),
            padding=ft.padding.only(top=10),
            bgcolor=ft.Colors.AMBER_100
        )

        # Register Tab
        register_tab = ft.Container(
            content=ft.Column([
                self.register_name,
                self.register_email,
                self.register_password,
                ft.Container(height=10),
                ft.Row([
                    ft.FilledButton("Register", on_click=self.handle_register, expand=True,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=15),
            padding=ft.padding.only(top=10)
        )

        # Main Content
        self.content = ft.Container(
            padding=ft.padding.symmetric(vertical=20, horizontal=25),
            content=ft.Column([
                ft.Text("UniProject Finder", size=24, weight=ft.FontWeight.W_800, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY_700),
                ft.Text("Discover projects that match your skills", color=ft.Colors.GREY_700),
                ft.Container(height=10),
                self.error_message,
                ft.Tabs(
                    selected_index=0,
                    tabs=[
                        ft.Tab(text="Login", content=login_tab),
                        ft.Tab(text="Register", content=register_tab),
                    ],
                    animation_duration=0
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
        )

    def show_error(self, msg):
        self.error_message.value = msg
        self.error_message.visible = True
        self.update()

    def hide_error(self, e=None):
        self.error_message.visible = False
        self.update()

    def handle_login(self, e):
        self.hide_error()
        time.sleep(0.5)
        email = self.login_email.value
        pwd = self.login_password.value
        if not email or not pwd:
            self.show_error("Email and password required")
            return
        user = mock_auth_login(email, pwd)
        if user:
            self.on_auth_success(user)
        else:
            self.show_error("Invalid credentials")

    def handle_register(self, e):
        self.hide_error()
        name = self.register_name.value
        email = self.register_email.value
        pwd = self.register_password.value
        if not all([name, email, pwd]):
            self.show_error("All fields required")
            return
        user = mock_auth_register(email, pwd, name)
        if user:
            self.on_auth_success(user)
        else:
            self.show_error("Email already exists")


