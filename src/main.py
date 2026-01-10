import flet as ft
from components.AuthForm import AuthForm
from components.Header import Header
from components.WelcomeScreen import WelcomeScreen
from components.LearningPath import LearningPath
from components.PathDialog import PathDialog
from logic import UserInfo, Suggestion
from logic.ProjectInfo import ProjectInfo
from data.fb import fb_update, get_all_projects
from services.FavService import FavService
from components.ProjectCard import ProjectCard
from components.ProjectDetailsDialog import ProjectDetailsDialog

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
        page.spacing = 0
        self.user = None
        self.fav_service = None
        self.all_projects = None
        self.current_view = "learningPath"
        self.screen = ft.Container(expand=True)
        page.add(self.screen)

        self.path_dialog = ft.Container()
        self.show_auth()

    def show_auth(self):
        self.user = None
        self.fav_service = None
        self.all_projects = None
        self.screen.content = AuthForm(self.login)
        self.screen.alignment = ft.alignment.center
        self.page.update()

    def login(self, user):
        self.user = user
        self.fav_service = FavService(user)
        self.all_projects = get_all_projects()
        self.current_view = "learningPath"
        self.show_main()

    def show_main(self):
        def set_view(v):
            self.current_view = v
            self.update_main()

        def logout():
            self.show_auth()

        print("DEBUG USER DATA:", self.user)
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
                raw_projs = self.user.get("proj", [])
                norm_projs = []
                for p in raw_projs:
                    if isinstance(p, ProjectInfo):
                        norm_projs.append(p)
                    elif isinstance(p, dict):
                        try:
                            norm_projs.append(ProjectInfo(**p))
                        except Exception:
                            continue
                content = LearningPath(
                    user=self.user,
                    projs=norm_projs,
                    on_generate_new=self.open_generate_dialog,
                    fav_service=self.fav_service,
                )
        elif self.current_view == "solved":
            all_norm_projs = []
            for p in self.all_projects:
                if isinstance(p, ProjectInfo):
                    all_norm_projs.append(p)
                elif isinstance(p, dict):
                    try:
                        all_norm_projs.append(ProjectInfo(**p))
                    except Exception:
                        continue
            
            solved_projs = [p for p in all_norm_projs if p.title in self.user.get("completedProjects", [])]
            
            if not solved_projs:
                content = ft.Container(
                    content=ft.Text("No solved projects yet.", size=24),
                    expand=True, alignment=ft.alignment.center
                )
            else:
                project_cards = []
                for i, project in enumerate(solved_projs):
                    card = ProjectCard(
                        project=project,
                        is_favorite=self.fav_service.is_favorite(project.title),
                        on_toggle_favorite=lambda pid=project.title: self.toggle_fav(pid),
                        on_view_details=lambda p=project: self.open_detail(p),
                        is_locked=False,
                        is_completed=True,
                        order_number=i,
                    )
                    project_cards.append(card)

                content = ft.Column(
                    project_cards,
                    spacing=16,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
        else:  # favorites
            all_norm_projs = []
            for p in self.all_projects:
                if isinstance(p, ProjectInfo):
                    all_norm_projs.append(p)
                elif isinstance(p, dict):
                    try:
                        all_norm_projs.append(ProjectInfo(**p))
                    except Exception:
                        continue
            
            faved_projs = [p for p in all_norm_projs if self.fav_service.is_favorite(p.title)]
            
            if not faved_projs:
                content = ft.Container(
                    content=ft.Text("No favorite projects yet.", size=24),
                    expand=True, alignment=ft.alignment.center
                )
            else:
                project_cards = []
                for i, project in enumerate(faved_projs):
                    card = ProjectCard(
                        project=project,
                        is_favorite=True,
                        on_toggle_favorite=lambda pid=project.title: self.toggle_fav(pid),
                        on_view_details=lambda p=project: self.open_detail(p),
                        is_locked=False,
                        is_completed=project.title in self.user.get("completedProjects", []),
                        order_number=i,
                    )
                    project_cards.append(card)

                content = ft.Column(
                    project_cards,
                    spacing=16,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )

        self.screen.content = ft.Column([header, content],expand_loose=True, alignment = ft.MainAxisAlignment.START, expand=True)
        self.page.update()

    def toggle_fav(self, pid):
        self.fav_service.toggle_favorite(pid)
        self.update_main()

    def open_detail(self, project):
        is_done = project.title in self.user.get("completedProjects", [])
        dialog = ProjectDetailsDialog(
            project=project,
            is_done=is_done,
            fav_service=self.fav_service,
            on_close=self.close_dialog,
            on_mark_complete=self.mark_complete,
        )
        self.page.dialog = dialog
        self.page.overlay.append(self.page.dialog)
        self.page.dialog.open = True
        self.page.update()
    
    def mark_complete(self, pid):
        if pid not in self.user.get("completedProjects", []):
            self.user["completedProjects"].append(pid)
        uid = self.user.get("localId")
        id_token = self.user.get("idToken")
        if uid and id_token:
            try:
                fb_update(
                    path=f"users/{uid}",
                    data={"completedProjects": self.user["completedProjects"]},
                    id_token=id_token,
                )
            except Exception as _:
                pass
        self.close_dialog()
        self.update_main()

    def update_main(self):
        self.show_main()

    def open_generate_dialog(self, e=None):
        self.path_dialog =  PathDialog(
                page=self.page,
                on_path_generated=self.on_path_generated,
                on_close=self.close_dialog,
            )

        self.path_dialog.show()

    def close_dialog(self, e=None):
        self.page.dialog.open = False
        self.page.update()
        
    def on_path_generated(self, path):
        completed_projects = self.user.get("completedProjects", [])
        projects = Suggestion.Suggestion().ProjectSuggestList(path, completed_projects=completed_projects)
        self.user["proj"] = projects
        self.user["hasGeneratedPath"] = True
        uid = self.user.get("localId")
        id_token = self.user.get("idToken")
        if uid and id_token:
            try:
                fb_update(
                    path=f"users/{uid}",
                    data={
                        "hasGeneratedPath": True,
                        "proj": [p.to_dict() for p in projects],
                    },
                    id_token=id_token,
                )
            except Exception:
                pass

        self.update_main()

def main(page: ft.Page):
    App(page)

ft.app(target=main)
