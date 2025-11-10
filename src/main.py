import flet as ft
from components.AuthForm import AuthForm
from components.Header import Header
from components.WelcomeScreen import WelcomeScreen
from components.LearningPath import LearningPath
from components.PathDialog import PathDialog

# Sample path data
SAMPLE_PATH = {
    "name": "Web Development Path",
    "description": "From HTML basics to full-stack apps",
    "projects": [
        {"id": "p1", "title": "Static Page", "description": "Build a simple HTML page", "prerequisite": None},
        {"id": "p2", "title": "Interactive Todo", "description": "Add JS interactivity", "prerequisite": "p1"},
        {"id": "p3", "title": "API Backend", "description": "Connect to a mock API", "prerequisite": "p2"},
    ]
}

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        page.title = "UniProject Finder"
        page.bgcolor = ft.Colors.GREY_50
        page.padding = 0

        self.user = None
        self.current_view = "learningPath"
        self.screen = ft.Container(expand=True)
        page.add(self.screen)

        self.dialog = PathDialog(
            on_path_generated=self.on_path_generated,
            on_close=lambda: self.close_dialog(),
            preselected_skills=[]
        )
        self.show_auth()

    def show_auth(self):
        self.user = None
        self.screen.content = AuthForm(self.login)
        self.screen.alignment = ft.alignment.center
        self.page.update()

    def login(self, user):
        self.user = user
        self.current_view = "learningPath"
        self.show_main()

    def show_main(self):
        def set_view(v):
            self.current_view = v
            self.update_main()

        def logout():
            self.show_auth()

        header = Header(
            user=self.user,
            on_logout=logout,
            current_view=self.current_view,
            on_view_change=set_view,
        )

        if self.current_view == "learningPath":
            if not self.user.get("hasGeneratedPath", False):
                content = WelcomeScreen(self.open_generate_dialog)
            else:
                content = LearningPath(
                    user=self.user,
                    path=SAMPLE_PATH,
                    on_generate_new=self.open_generate_dialog,
                )
        else:  # favorites
            content = ft.Container(
                content=ft.Text("Favorites coming soon", size=24),
                expand=True, alignment=ft.alignment.center
            )

        self.screen.content = ft.Column([header, content], expand=True, spacing=0)
        self.page.update()

    def update_main(self):
        self.show_main()

    def open_generate_dialog(self, e=None):
        # Add to overlay (works on every platform)
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    # ------------------------------------------------------------------
    def close_dialog(self, e=None):
        """Remove dialog **and** its backdrop."""
        if hasattr(self, "dialog") and self.dialog in self.page.overlay:
            self.page.overlay.remove(self.dialog)

        # Remove the dark backdrop (GestureDetector)
        self.dialog.open = False
        self.page.overlay.clear()
        self.page.update()
    def on_path_generated(self, path):
        self.user["path"] = path
        self.user["hasGeneratedPath"] = True
        self.page.show_snack_bar(ft.SnackBar(ft.Text("Learning path generated!")))
        self.update_main()

def main(page: ft.Page):
    App(page)

ft.app(target=main)
