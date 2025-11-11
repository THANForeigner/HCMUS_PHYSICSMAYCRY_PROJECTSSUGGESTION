from os import name
import flet as ft
from components import ProjectCard
from logic.ProjectInfo import ProjectInfo
from libs import AuthService
from libs import FavService

class LearningPath(ft.Container):
    def __init__(self, user, projs:list[ProjectInfo], on_generate_new):
        super().__init__(padding=ft.padding.symmetric(horizontal=16, vertical=32), expand=True)
        self.user = user
        self.projs = projs
        self.on_generate_new = on_generate_new

        # State
        self.favorites = FavService.get_favorites()
        self.completed = user.get("completedProjects", [])
        self.selected_project = None

        self.build_ui()

    def build_ui(self):
        total = len(self.projs)
        done = len([p for p in self.projs if p.title in self.completed])
        percent = int((done / total) * 100) if total else 0

        header_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.CANDLESTICK_CHART, color=ft.Colors.INDIGO_600, size=20),
                                ft.Text("This is your learning path", size=20, weight=ft.FontWeight.BOLD)
                            ], spacing=8),
                            ft.Text("hoho", color=ft.Colors.GREY_600),
                        ], expand=True),
                        ft.OutlinedButton(
                            "Generate New Path",
                            icon=ft.Icons.CANDLESTICK_CHART,
                            on_click=lambda _: self.on_generate_new(),
                        ),
                    ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=16),
                    ft.Column([
                        ft.Row([
                            ft.Text("Progress", color=ft.Colors.GREY_600),
                            ft.Text(f"{done} / {total} projects completed", weight=ft.FontWeight.BOLD)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.ProgressBar(value=percent / 100, height=12, bgcolor=ft.Colors.GREY_300),
                    ], spacing=8),
                ], spacing=16),
                padding=24,
            )
        )

        # Completion Banner
        completion_banner = None
        if done == total:
            completion_banner = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.TRANSCRIBE_SHARP, size=48, color=ft.Colors.GREEN_600),
                    ft.Text("Congratulations!", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900),
                    ft.Text("You've completed all projects!", color=ft.Colors.GREEN_700),
                    ft.ElevatedButton(
                        "Start New Learning Path",
                        icon=ft.Icons.TOPIC,
                        on_click=lambda _: self.on_generate_new(),
                        bgcolor=ft.Colors.INDIGO_600,
                        color=ft.Colors.WHITE,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400),
                border=ft.border.all(1, ft.Colors.GREEN_200),
                border_radius=12,
                padding=24,
                alignment=ft.alignment.center,
            )

        # Projects List
        project_cards = []
        for i, project in enumerate(self.projs):
            is_locked =( i > 0 and self.projs[i-1].title not in self.completed)
            is_done = project.title in self.completed
            is_fav = project.title in self.favorites

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
                        content=ft.Icon(ft.Icons.ARROW_DOWNWARD, size=24, color=ft.Colors.GREY_300),
                        alignment=ft.alignment.center,
                        height=40,
                    )
                )
            project_cards.append(ft.Container(wrapper, alignment=ft.alignment.center))

        # Main Content
        self.content = ft.Column([
            header_card,
            completion_banner or ft.Container(),
            ft.Container(height=24),
            ft.Text("Projects", size=18, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Complete each project in order to unlock the next one. Projects get progressively harder as you advance.",
                color=ft.Colors.GREY_600
            ),
            ft.Container(height=16),
            ft.Column(project_cards, spacing=0, scroll=ft.ScrollMode.AUTO),
            self.build_dialog(),
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    def toggle_fav(self, pid):
        FavService.toggle_favorite(pid)
        self.favorites = FavService.get_favorites()
        self.page.update()

    def open_detail(self, project):
        self.selected_project = project
        self.page.dialog = self.build_dialog()
        self.page.overlay.append(self.page.dialog)
        self.page.dialog.open = True
        self.page.update()

    def build_dialog(self):
        if not self.selected_project:
            return ft.Container()

        project: ProjectInfo = self.selected_project
        is_fav   = project.title in self.favorites
        is_done  = project.title in self.completed

        return ft.AlertDialog(
                modal=True,
                shape=ft.RoundedRectangleBorder(radius=16),
                bgcolor=ft.Colors.WHITE,
                
                title=ft.Row(
                    [
                        ft.Text(project.title, weight=ft.FontWeight.BOLD, size=20, expand=True, color=ft.Colors.BLACK),
                        ft.IconButton(ft.Icons.CLOSE, on_click=lambda _: self.close_dialog(), icon_color=ft.Colors.GREY_600),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                # --- 2. CONTENT ---
                content=ft.Container(
                    width=560,
                    height=400, # Set a height to make the column scrollable
                    content=ft.Column(
                        [
                            ft.Text(project.description, size=14, color=ft.Colors.GREY_700),
                            
                            ft.Divider(height=20),

                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Row([ft.Icon(ft.Icons.SCHOOL_OUTLINED, color=ft.Colors.GREY_500, size=16), ft.Text("Major", size=12, color=ft.Colors.GREY_500)], spacing=4),
                                            ft.Text(project.major or "—", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                        ],
                                        expand=True,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Row([ft.Icon(ft.Icons.TIMER_OUTLINED, color=ft.Colors.GREY_500, size=16), ft.Text("Est. Time", size=12, color=ft.Colors.GREY_500)], spacing=4),
                                            ft.Text(f"{project.estimated_hours} hours", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                        ],
                                        expand=True,
                                    ),
                                ],
                                spacing=16,
                            ),
                            
                            ft.Divider(height=20),

                            ft.Text("Skills", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLACK),
                            ft.Container(height=4),
                            ft.Row(
                                [
                                    ft.Chip(
                                        label=ft.Text(s, color=ft.Colors.BLACK, weight=ft.FontWeight.W_400, size=16), 
                                        color= ft.Colors.GREY_500
                                    ) for s in project.skills
                                ],
                                wrap=True,
                                spacing=6,
                                run_spacing=6,
                            ),
                            
                            ft.Container(height=16), 

                            ft.Text("Requires", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLACK),
                            ft.Container(height=4),
                            ft.Row(
                                [
                                    ft.Chip(
                                        label=ft.Text(project.required_material, color=ft.Colors.BLACK, weight=ft.FontWeight.W_400, size=16), 
                                        color= ft.Colors.GREY_500
                                    ) 
                                ],
                                wrap=True, 
                                spacing=6,
                                run_spacing=6,
                            ),

                        ],
                        scroll=ft.ScrollMode.AUTO,
                        spacing=12
                    ),
                    padding=ft.padding.only(top=0, bottom=12, left=4, right=4) # Add padding to content
                ),
                
                # --- 3. ACTIONS ---
                # Use the 'actions' slot for the buttons
                actions=[
                    ft.TextButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.BOOKMARK if is_fav else ft.Icons.BOOKMARK_BORDER, color=ft.Colors.INDIGO_600),
                                ft.Text("Favorite", color=ft.Colors.INDIGO_600)
                            ], 
                            spacing=4
                        ),
                        on_click=lambda _: self.toggle_fav(project.title),
                    ),
                    ft.FilledButton(
                        "Mark Complete",
                        icon=ft.Icons.CHECK,
                        on_click=lambda _: self.mark_complete(project.title),
                        disabled=is_done,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.INDIGO_600 if not is_done else ft.Colors.GREY_300,
                            color=ft.Colors.WHITE if not is_done else ft.Colors.GREY_500,
                        )
                    ),
                ],
                actions_padding=ft.padding.only(bottom=16, right=24),
                content_padding=ft.padding.all(24),
                title_padding=ft.padding.all(24),
            )          

    def mark_complete(self, pid):
        AuthService.complete_project(pid)
        self.completed.append(pid)
        self.close_dialog()
        self.build_ui()
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()
