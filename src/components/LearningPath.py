import flet as ft
from components import ProjectCard
from logic.ProjectInfo import ProjectInfo
from services import AuthService
from services import FavService
from components.ProjectDetailsDialog import ProjectDetailsDialog
from data.fb import fb_update


class LearningPath(ft.Container):
    def __init__(self, user, projs: list[ProjectInfo], on_generate_new, fav_service):
        super().__init__(
            padding=ft.padding.symmetric(horizontal=16, vertical=32), expand=True
        )
        self.user = user
        self.on_generate_new = on_generate_new
        self.fav_service = fav_service

        # Sort projects by difficulty
        self.projs = sorted(projs, key=lambda p: (len(p.skills), p.estimated_hours))

        # State
        self.completed = user.get("completedProjects", [])
        self.selected_project = None

        self.build_ui()

    def build_ui(self):
        total = len(self.projs)
        done = len([p for p in self.projs if p.title in self.completed])
        percent = int((done / total) * 100) if total else 0

        header_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(
                                                    ft.Icons.CANDLESTICK_CHART,
                                                    color=ft.Colors.INDIGO_600,
                                                    size=20,
                                                ),
                                                ft.Text(
                                                    "This is your learning path",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ],
                                            spacing=8,
                                        ),
                                        ft.Text(
                                            "Your progress at a glance",
                                            color=ft.Colors.GREY_600,
                                        ),
                                    ],
                                    expand=True,
                                ),
                                ft.OutlinedButton(
                                    "Generate New Path",
                                    icon=ft.Icons.CANDLESTICK_CHART,
                                    on_click=lambda _: self.on_generate_new(),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=16),
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text("Progress", color=ft.Colors.GREY_600),
                                        ft.Text(
                                            f"{done} / {total} projects completed",
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.ProgressBar(
                                    value=percent / 100,
                                    height=12,
                                    bgcolor=ft.Colors.GREY_300,
                                ),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=16,
                ),
                padding=24,
            )
        )

        # Completion Banner
        completion_banner = None
        if done == total:
            completion_banner = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.TRANSCRIBE_SHARP,
                            size=48,
                            color=ft.Colors.GREEN_600,
                        ),
                        ft.Text(
                            "Congratulations!",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_900,
                        ),
                        ft.Text(
                            "You've completed all projects!", color=ft.Colors.GREEN_700
                        ),
                        ft.ElevatedButton(
                            "Start New Learning Path",
                            icon=ft.Icons.TOPIC,
                            on_click=lambda _: self.on_generate_new(),
                            bgcolor=ft.Colors.INDIGO_600,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400),
                border=ft.border.all(1, ft.Colors.GREEN_200),
                border_radius=12,
                padding=24,
                alignment=ft.alignment.center,
            )

        # Projects List
        project_cards = []
        for i, project in enumerate(self.projs):
            is_locked = i > 0 and self.projs[i - 1].title not in self.completed
            is_done = project.title in self.completed
            is_fav = self.fav_service.is_favorite(project.title)

            card = ProjectCard.ProjectCard(
                project=project,
                is_favorite=is_fav,
                on_toggle_favorite=lambda pid=project.title: self.toggle_fav(pid),
                on_view_details=lambda p=project: self.open_detail(p),
                is_locked=is_locked,
                is_completed=is_done,
                order_number=i,
            )

            # Arrow between cards
            wrapper = ft.Column([card])
            if i < len(self.projs) - 1:
                wrapper.controls.append(
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.ARROW_DOWNWARD, size=24, color=ft.Colors.GREY_300
                        ),
                        alignment=ft.alignment.center,
                        height=40,
                    )
                )
            project_cards.append(ft.Container(wrapper, alignment=ft.alignment.center))

        # Main Content
        self.content = ft.Column(
            [
                header_card,
                completion_banner or ft.Container(),
                ft.Container(height=24),
                ft.Text("Projects", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Complete each project in order to unlock the next one. Projects get progressively harder as you advance.",
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(height=16),
                ft.Column(project_cards, spacing=0, scroll=ft.ScrollMode.AUTO),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def toggle_fav(self, pid):
        self.fav_service.toggle_favorite(pid)
        self.build_ui()
        self.page.update()

    def open_detail(self, project):
        is_done = project.title in self.completed
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
        if pid not in self.completed:
            self.completed.append(pid)
        uid = self.user.get("localId")
        id_token = self.user.get("idToken")
        if uid and id_token:
            try:
                fb_update(
                    path=f"users/{uid}",
                    data={"completedProjects": self.completed},
                    id_token=id_token,
                )
            except Exception as _:
                pass
        self.close_dialog()
        self.build_ui()
        self.page.update()

    def close_dialog(self, e=None):
        self.page.dialog.open = False
        self.page.update()
