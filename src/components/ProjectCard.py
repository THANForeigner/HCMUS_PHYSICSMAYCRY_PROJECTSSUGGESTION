import flet as ft

class ProjectCard(ft.Card):
    def __init__(self, project, is_favorite, on_toggle_favorite, on_view_details, is_locked, is_completed, order_number):
        super().__init__(
            elevation=2,
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text(str(order_number + 1), size=18, weight=ft.FontWeight.BOLD),
                            width=40, height=40,
                            bgcolor=ft.Colors.INDIGO_100 if not is_locked else ft.Colors.GREY_300,
                            border_radius=20,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column([
                            ft.Text(project["title"], weight=ft.FontWeight.BOLD),
                            ft.Text(project["description"][:100] + "...", color=ft.Colors.GREY_600),
                        ], expand=True),
                        ft.Column([
                            ft.IconButton(
                                ft.Icons.BOOKMARK if is_favorite else ft.Icons.BOOKMARK_BORDER,
                                on_click=lambda _: on_toggle_favorite(),
                                tooltip="Favorite"
                            ),
                            ft.Icon(ft.Icons.LOCK if is_locked else ft.Icons.CHECK_CIRCLE,
                                    color=ft.Colors.GREY_400 if is_locked else ft.Colors.GREEN_600),
                        ], spacing=0),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=8),
                    ft.ElevatedButton(
                        "View Details",
                        on_click=lambda _: on_view_details(),
                        disabled=is_locked,
                    ),
                ], spacing=12),
                padding=20,
                on_click=lambda _: on_view_details() if not is_locked else None,
            ),
            opacity=0.6 if is_locked else 1.0,
        )
