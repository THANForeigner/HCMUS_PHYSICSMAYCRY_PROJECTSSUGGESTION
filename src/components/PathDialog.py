# components/generate_path_alog.py
import flet as ft

all_skills = ["Python", "JavaScript", "React", "Node.js", "SQL", "Docker"]

class PathDialog(ft.AlertDialog):
    def __init__(self, on_path_generated, on_close, preselected_skills=None):
        self.on_path_generated = on_path_generated
        self.on_close = on_close
        self.preselected = preselected_skills or []
        self.selected_skills = self.preselected[:]
        self.is_generating = False

        # Build UI
        title = ft.Row([
            ft.Icon(ft.Icons.STARS, color=ft.Colors.INDIGO_600, size=20),
            ft.Text("Generate Learning Path", weight=ft.FontWeight.BOLD)
        ], spacing=8)

        # Buttons (create early so we can reference in actions)
        self.generate_btn = ft.FilledButton(
            "Generate Path",
            icon=ft.Icons.STARS,
            on_click=self.handle_generate,
            style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_600),
            expand=True,
        )
        self.cancel_btn = ft.OutlinedButton(
            "Cancel",
            on_click=self.handle_close,
            expand=True,
        )

        # Main content
        self.loading_indicator = ft.Row([
            ft.ProgressRing(width=16, height=16, stroke_width=2),
            ft.Text("Generating Path...", color=ft.Colors.INDIGO_700)
        ], spacing=8, visible=False)

        content_column = ft.Column([
            ft.Text("Select up to 3 skills to generate a personalized progressive learning path", color=ft.Colors.GREY_600),
            ft.Container(height=16),
            ft.Text(f"Selected Skills ({len(self.selected_skills)}/3)", weight=ft.FontWeight.BOLD),
            ft.Row(
                [self._make_skill_badge(s) for s in all_skills],
                wrap=True, spacing=8, run_spacing=8
            ),
            ft.Container(height=24),
            self._make_info_box(),
            ft.Container(height=24),
            self.loading_indicator
        ], scroll=ft.ScrollMode.AUTO)

        # Now initialize AlertDialog with full content
        super().__init__(
            modal=True,
            title=title,
            content=ft.Container(content_column, width=600, padding=20),
            actions=[self.generate_btn, self.cancel_btn],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=on_close,
        )

        # Update button state
        self.update_generate_button()

    def _make_skill_badge(self, skill):
        is_selected = skill in self.selected_skills
        can_select = len(self.selected_skills) < 3 or is_selected

        return ft.Container(
            content=ft.Row([
                ft.Text(skill, size=13),
                ft.Icon(ft.Icons.CHECK, size=14, visible=is_selected)
            ], spacing=4, tight=True),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            bgcolor=ft.Colors.INDIGO_600 if is_selected else ft.Colors.TRANSPARENT,
            border=ft.border.all(1, ft.Colors.INDIGO_600 if is_selected else ft.Colors.GREY_400),
            border_radius=20,
            on_click=lambda e, s=skill: self.toggle_skill(s) if can_select else None,
            opacity=0.5 if not can_select and not is_selected else 1.0,
        )

    def _make_info_box(self):
        return ft.Container(
            bgcolor=ft.Colors.INDIGO_50,
            border=ft.border.all(1, ft.Colors.INDIGO_200),
            border_radius=8,
            padding=16,
            content=ft.Column([
                ft.Text("What to expect:", weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
                ft.Column([
                    ft.Row([ft.Text("•", color=ft.Colors.INDIGO_600), ft.Text("5 progressive projects...", color=ft.Colors.INDIGO_700)], spacing=8),
                    ft.Row([ft.Text("•", color=ft.Colors.INDIGO_600), ft.Text("Each project unlocks...", color=ft.Colors.INDIGO_700)], spacing=8),
                    ft.Row([ft.Text("•", color=ft.Colors.INDIGO_600), ft.Text("Tailored to your skills...", color=ft.Colors.INDIGO_700)], spacing=8),
                ], spacing=4),
            ], spacing=8),
        )

    def toggle_skill(self, skill):
        if skill in self.selected_skills:
            self.selected_skills.remove(skill)
        elif len(self.selected_skills) < 3:
            self.selected_skills.append(skill)
        self.update_generate_button()
        self.page.update()

    def update_generate_button(self):
        has_skills = len(self.selected_skills) > 0
        self.generate_btn.disabled = not has_skills or self.is_generating
        self.cancel_btn.disabled = self.is_generating

    def handle_generate(self, e):
        if not self.selected_skills or self.is_generating: return
        self.is_generating = True
        self.loading_indicator.visible = True
        self.update_generate_button()
        self.page.update()

        def generate():
            import time
            time.sleep(2)
            path = {
                "name": f"{', '.join(self.selected_skills)} Path",
                "description": "Custom path",
                "projects": [{"id": f"p{i}", "title": f"Project {i}", "prerequisite": f"p{i-1}" if i > 1 else None} for i in range(1, 6)]
            }
            self.page.call_in_main_thread(self.finish_generation, path)

        self.page.run_thread(generate)

    def finish_generation(self, path):
        self.is_generating = False
        self.loading_indicator.visible = False
        self.on_path_generated(path)
        self.handle_close(None)

    def handle_close(self, e):
        self.selected_skills = []
        self.on_close()
