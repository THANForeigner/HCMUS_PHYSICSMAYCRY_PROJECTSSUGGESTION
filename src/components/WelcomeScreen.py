import flet as ft

class WelcomeScreen(ft.Container):
    def __init__(self, on_generate_path):
        super().__init__(
            padding=ft.padding.symmetric(vertical=64, horizontal=16),
            expand=True,
            alignment=ft.alignment.center,
        )

        # Icon Circle
        icon_circle = ft.Container(
            content=ft.Icon(ft.Icons.SPOKE_SHARP, size=40, color=ft.Colors.INDIGO_600),
            width=80, height=80,
            bgcolor=ft.Colors.INDIGO_100,
            border_radius=40,
            alignment=ft.alignment.center,
        )

        # Cards
        card1 = self._make_card(
            icon=ft.Icons.ABC_ROUNDED,
            title="Progressive Learning",
            desc="Start with beginner projects and unlock harder ones as you complete each step. Build your skills gradually with structured progression."
        )
        card2 = self._make_card(
            icon=ft.Icons.BOOK,
            title="Skill-Based Projects",
            desc="Projects are generated based on your selected skills and interests. Each project includes learning objectives and recommended resources."
        )

        # Gradient Card
        gradient_card = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.INDIGO_300),
            border=ft.border.all(1, ft.Colors.INDIGO_200),
            border_radius=12,
            padding=24,
            width=800,
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.Text("Ready to Start Your Learning Journey?",color=ft.Colors.GREY_700, size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Click below to select your skills and generate your first personalized learning path", color=ft.Colors.GREY_500),
                ft.Container(height=16),
                ft.ElevatedButton(
                    "Generate My Learning Path",
                    icon=ft.Icons.CANDLESTICK_CHART_ROUNDED,
                    on_click=lambda e: on_generate_path(),
                    bgcolor=ft.Colors.BLACK,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=24, vertical=14)),
                ),
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8),
        )

        # Info Box
        info_box = ft.Container(
            bgcolor=ft.Colors.AMBER_50,
            border=ft.border.all(1, ft.Colors.AMBER_200),
            border_radius=8,
            padding=16,
            content=ft.Text(
                "How it works: Select up to 3 skills → AI generates 5 progressive projects → "
                "Complete projects in order from easy to advanced → Unlock new projects as you progress",
                color=ft.Colors.AMBER_900,
                weight=ft.FontWeight.W_700,
            ),
        )

        # Layout
        self.content = ft.Column([
            ft.Column([
                icon_circle,
                ft.Text("Welcome to UniProject Finder", size=28,color=ft.Colors.GREY_700, weight=ft.FontWeight.W_800, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    "Generate a personalized learning path tailored to your skills and goals. "
                    "Our AI will create progressive projects from beginner to advanced.",
                    color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),

            ft.Container(height=32),

            ft.Row([card1, card2], spacing=24, alignment=ft.MainAxisAlignment.CENTER, wrap=True),

            ft.Container(height=32),

            gradient_card,

            ft.Container(height=24),

            info_box,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

    def _make_card(self, icon, title, desc):
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            padding=20,
            width=350,
            height=200,
            content=ft.Column([
                ft.Icon(icon, size=32, color=ft.Colors.INDIGO_600),
                ft.Container(height=8),
                ft.Text(title, size=16, color=ft.Colors.GREY_500, weight=ft.FontWeight.BOLD),
                ft.Text(desc, color=ft.Colors.GREY_600),
            ], spacing=4),
        )
