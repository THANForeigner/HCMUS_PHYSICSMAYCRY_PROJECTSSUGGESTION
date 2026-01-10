import flet as ft


class Header(ft.Container):
    def __init__(self, user, on_logout, current_view, on_view_change):
        super().__init__(
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300)),
            padding=ft.padding.symmetric(vertical=16, horizontal=20),
        )

        learning_btn = ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CAMPAIGN, size=16),
                    ft.Text("Learning Path", weight=ft.FontWeight.BOLD),
                ],
                spacing=8,
            ),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.INDIGO_600
                if current_view == "learningPath"
                else None,
                color=ft.Colors.BLACK
                if current_view == "learningPath"
                else ft.Colors.GREY_700,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
            ),
            on_click=lambda _: on_view_change("learningPath"),
        )
        favorites_btn = ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.BOOKMARK, size=16),
                    ft.Text("Favorites", weight=ft.FontWeight.BOLD),
                ],
                spacing=8,
            ),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.INDIGO_600 if current_view == "favorites" else None,
                color=ft.Colors.BLACK
                if current_view == "favorites"
                else ft.Colors.GREY_700,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
            ),
            on_click=lambda _: on_view_change("favorites"),
        )
        solved_btn = ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=16),
                    ft.Text("Solved", weight=ft.FontWeight.BOLD),
                ],
                spacing=8,
            ),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.INDIGO_600 if current_view == "solved" else None,
                color=ft.Colors.BLACK
                if current_view == "solved"
                else ft.Colors.GREY_700,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
            ),
            on_click=lambda _: on_view_change("solved"),
        )

        user_info = ft.Column(
            [
                ft.Text(
                    user["name"],
                    size=14,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.RIGHT,
                ),
                ft.Text(
                    user["email"],
                    size=12,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.RIGHT,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        )

        logout_btn = ft.OutlinedButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.LOGOUT, size=16), ft.Text("Logout")], spacing=8
            ),
            on_click=lambda _: on_logout(),
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, ft.Colors.GREY_400),
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
            ),
        )

        self.content = ft.Row(
            controls=[
                ft.Row(
                    [
                        ft.Text(
                            "UniProject Finder",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.INDIGO_600,
                        ),
                        ft.Row([learning_btn, favorites_btn, solved_btn], spacing=8),
                    ],
                    spacing=24,
                    expand=True,
                ),
                ft.Row([user_info, logout_btn], spacing=16),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
