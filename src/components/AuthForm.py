import flet as ft
from data.fb import firebase_register, firebase_login, firebase_forgot_password, create_new_user_profile, get_user_profile

class AuthForm(ft.Container):
    def __init__(self, on_auth_success):
        super().__init__(
            width=420,
            bgcolor=ft.Colors.WHITE,
            padding=0,
            border_radius=10,
        )
        self.on_auth_success = on_auth_success

        self.login_email = ft.TextField(label="Email", text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                        hint_text="student@university.edu", on_change=self.hide_error)
        self.login_password = ft.TextField(label="Password", text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                           password=True, can_reveal_password=True, on_change=self.hide_error)
        self.login_password = ft.TextField(label="Password", text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                           password=True, can_reveal_password=True, on_change=self.hide_error)
        self.register_name = ft.TextField(label="Full Name", text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                          hint_text="John Doe", on_change=self.hide_error)
        self.register_email = ft.TextField(label="Email", text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                           hint_text="student@university.edu", on_change=self.hide_error)
        self.register_password = ft.TextField(label="Password", text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                              password=True, can_reveal_password=True, on_change=self.hide_error)

        self.error_message = ft.Text("", color=ft.Colors.RED_500, visible=False, text_align=ft.TextAlign.CENTER)
        self.message = ft.Text("", color=ft.Colors.BLACK, visible=False, text_align=ft.TextAlign.CENTER)

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
            bgcolor=ft.Colors.AMBER_50
        )

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
        forgot_password_tab = ft.Container(
            content=ft.Column([
                self.login_email,
                ft.Container(height=10),
                ft.Row([
                    ft.FilledButton("Enter", on_click=self.handle_forgot_password, expand=True,
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                self.message
            ], spacing=15),
            padding=ft.padding.only(top=10),
            bgcolor=ft.Colors.AMBER_50
        )

        self.content = ft.Container(
            padding=ft.padding.symmetric(vertical=20, horizontal=25),
            content=ft.Column([
                ft.Text("UniProject Finder", size=24, weight=ft.FontWeight.W_800, text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.GREY_700),
                ft.Text("Discover projects that match your skills", color=ft.Colors.GREY_700),
                ft.Container(height=10),
                self.error_message,
                ft.Tabs(
                    selected_index=0,
                    tabs=[ft.Tab(text="Login", content=login_tab), ft.Tab(text="Register", content=register_tab),
                          ft.Tab(text="Forgot Password", content=forgot_password_tab),],
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
        email = self.login_email.value
        pwd = self.login_password.value
        
        if not email or not pwd:
            self.show_error("Please enter email and password")
            return

        auth_result = firebase_login(email, pwd)
        
        if "error" in auth_result:
            err_msg = auth_result["error"]
            # Firebase returns 'INVALID_LOGIN_CREDENTIALS' for wrong email or password
            if "INVALID_LOGIN_CREDENTIALS" in err_msg:
                self.show_error("Wrong email or password!")
            else:
                self.show_error(f"Login failed: {err_msg}")
            return
            
        self.on_auth_success(get_user_profile(auth_result))

    def handle_register(self, e):
        self.hide_error()
        name = self.register_name.value
        email = self.register_email.value
        pwd = self.register_password.value

        if not all([name, email, pwd]):
            self.show_error("All fields required")
            return

        result = firebase_register(email, pwd, name)

        if "error" in result:
            err = result["error"]
            # Firebase error for existing email is usually EMAIL_EXISTS
            if "EMAIL_EXISTS" in err:
                self.show_error("Email already used! Please try another.")
            else:
                self.show_error(err)
        else:
            self.on_auth_success(create_new_user_profile(result, name))
    def handle_forgot_password(self, e):
        self.message.visible = False
        self.update()
        self.hide_error()
        print("Forgot password?")
        email = self.login_email.value
        if not email:
            self.show_error("Email required")
            return
        oob_code = ""
        result = firebase_forgot_password(email)
        print(result)
        self.message.value = "Send email for reset password done!"
        self.message.visible = True
        self.update()

