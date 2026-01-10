import flet as ft
from logic.ProjectInfo import ProjectInfo
from services.FavService import FavService


class ProjectDetailsDialog(ft.AlertDialog):
    def __init__(
        self,
        project: ProjectInfo,
        is_done: bool,
        fav_service: FavService,
        on_close,
        on_mark_complete,
    ):
        super().__init__(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.WHITE,
        )
        self.project = project
        self.is_done = is_done
        self.fav_service = fav_service
        self.on_close = on_close
        self.on_mark_complete = on_mark_complete
        self.is_fav = self.fav_service.is_favorite(self.project.title)

        self.title = self._build_title()
        self.content = self._build_content()
        self.actions = self._build_actions()
        self.actions_padding = ft.padding.only(bottom=16, right=24)
        self.content_padding = ft.padding.all(24)
        self.title_padding = ft.padding.all(24)

    def _build_title(self):
        return ft.Row(
            [
                ft.Text(
                    self.project.title,
                    weight=ft.FontWeight.BOLD,
                    size=20,
                    expand=True,
                    color=ft.Colors.BLACK,
                ),
                ft.IconButton(
                    ft.Icons.CLOSE,
                    on_click=lambda _: self.on_close(),
                    icon_color=ft.Colors.GREY_600,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _build_content(self):
        return ft.Container(
            width=560,
            height=400,
            content=ft.Column(
                [
                    ft.Text(
                        self.project.description, size=14, color=ft.Colors.GREY_700
                    ),
                    ft.Divider(height=20),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(
                                                ft.Icons.SCHOOL_OUTLINED,
                                                color=ft.Colors.GREY_500,
                                                size=16,
                                            ),
                                            ft.Text(
                                                "Major",
                                                size=12,
                                                color=ft.Colors.GREY_500,
                                            ),
                                        ],
                                        spacing=4,
                                    ),
                                    ft.Text(
                                        self.project.major or "—",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK,
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(
                                                ft.Icons.TIMER_OUTLINED,
                                                color=ft.Colors.GREY_500,
                                                size=16,
                                            ),
                                            ft.Text(
                                                "Est. Time",
                                                size=12,
                                                color=ft.Colors.GREY_500,
                                            ),
                                        ],
                                        spacing=4,
                                    ),
                                    ft.Text(
                                        f"{self.project.estimated_hours} hours",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK,
                                    ),
                                ],
                                expand=True,
                            ),
                        ],
                        spacing=16,
                    ),
                    ft.Divider(height=20),
                    ft.Text(
                        "Skills",
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Container(height=4),
                    ft.Row(
                        [
                            ft.Chip(
                                label=ft.Text(
                                    s,
                                    color=ft.Colors.BLACK,
                                    weight=ft.FontWeight.W_400,
                                    size=16,
                                ),
                                color=ft.Colors.GREY_500,
                            )
                            for s in self.project.skills
                        ],
                        wrap=True,
                        spacing=6,
                        run_spacing=6,
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Requires",
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Container(height=4),
                    ft.Row(
                        [
                            ft.Chip(
                                label=ft.Text(
                                    self.project.required_material,
                                    color=ft.Colors.BLACK,
                                    weight=ft.FontWeight.W_400,
                                    size=16,
                                ),
                                color=ft.Colors.GREY_500,
                            )
                        ],
                        wrap=True,
                        spacing=6,
                        run_spacing=6,
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Tutorials",
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Container(height=4),
                    ft.Row(
                        [
                            ft.Chip(
                                label=ft.Text(
                                    link,
                                    color=ft.Colors.BLACK,
                                    weight=ft.FontWeight.W_400,
                                    size=16,
                                ),
                                on_click=lambda _, url=link: self.page.launch_url(url),
                                color=ft.Colors.GREY_500,
                            )
                            for link in self.project.tutorial_link
                        ],
                        wrap=True,
                        spacing=6,
                        run_spacing=6,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
            ),
            padding=ft.padding.only(top=0, bottom=12, left=4, right=4),
        )

    def _build_actions(self):
        return [
            ft.TextButton(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.BOOKMARK
                            if self.is_fav
                            else ft.Icons.BOOKMARK_BORDER,
                            color=ft.Colors.INDIGO_600,
                        ),
                        ft.Text("Favorite", color=ft.Colors.INDIGO_600),
                    ],
                    spacing=4,
                ),
                on_click=lambda _: self._toggle_fav(),
            ),
            ft.FilledButton(
                "Mark Complete",
                icon=ft.Icons.CHECK,
                on_click=lambda _: self.on_mark_complete(self.project.title),
                disabled=self.is_done,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.INDIGO_600
                    if not self.is_done
                    else ft.Colors.GREY_300,
                    color=ft.Colors.WHITE if not self.is_done else ft.Colors.GREY_500,
                ),
            ),
        ]

    def _toggle_fav(self):
        self.fav_service.toggle_favorite(self.project.title)
        self.is_fav = self.fav_service.is_favorite(self.project.title)
        self.actions = self._build_actions()
        self.update()
