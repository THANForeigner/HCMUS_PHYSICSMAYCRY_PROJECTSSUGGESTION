import flet as ft
from flet.auth.user import User
from data.const import interests, skills,major
from typing import Callable, List
from logic import UserInfo
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
class PathDialog:
    def __init__(
        self,
        page: ft.Page,
        on_path_generated: Callable[[dict], None],
        on_close: Callable[[], None],
    ):
        self.page = page
        self.on_path_generated = on_path_generated
        self.on_close = on_close

        # selected items
        self.skills: List[str] = []
        self.major: List[str] = []
        self.interests: List[str] = []

        # build UI
        # --- FIX 1: These are the placeholders ---
        self.skills_section = ft.Container()
        self.major_section = ft.Container()
        self.interests_section = ft.Container()
        # ----------------------------------------

        title = ft.Row([
            ft.Icon(ft.Icons.STARS, color=ft.Colors.INDIGO_600, size=24),
            ft.Text("Generate Learning Path", weight=ft.FontWeight.BOLD, size=18)
        ], spacing=8)

        # Buttons
        self.gen_btn = ft.FilledButton(
            "Generate Path",
            icon=ft.Icons.STARS,
            on_click=self._generate,
            expand=True,
            style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_600),
        )
        self.can_btn = ft.OutlinedButton(
            "Cancel", on_click=lambda _: self.close(), expand=True
        )
        # Main content
        self._content = ft.Container(
            ft.Column([
                title,
                ft.Text("Select your profile", color=ft.Colors.GREY_600),

                # --- FIX 1: Use the placeholders in the layout ---
                self.skills_section,
                self.major_section,
                self.interests_section,
                # -------------------------------------------------

                ft.Container(height=20),
                ft.Row([self.gen_btn, self.can_btn], spacing=12),
            ], scroll=ft.ScrollMode.AUTO),
            width=620,
            padding=24,
            bgcolor=ft.Colors.BLACK87,
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
        )
        self.backdrop:ft.Container = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
            expand=True,
            on_click=lambda _: self.close(),
        )

        # Full overlay
        self.overlay:ft.Stack = ft.Stack([
            self.backdrop,
            ft.Container(self._content, alignment=ft.alignment.center),
        ])

        # This will now correctly populate the placeholders
        self._refresh_all_sections()
        # Update button state
        self._update_generate_button()

    # ------------------------------------------------------------------
    def _section(self, title, items, selected, max_allowed, toggle_cb, single_select=False):
        return ft.Column([
            ft.Row([
                ft.Text(f"{title} ({len(selected)}/{max_allowed})", weight=ft.FontWeight.BOLD),
                ft.Text("(max)" if not single_select else "(choose one)", size=12, color=ft.Colors.GREY_600)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row(
                [self._badge(itm, itm in selected, lambda _, s=itm: toggle_cb(s),
                            disabled=(len(selected) >= max_allowed and itm not in selected) or
                                     (single_select and len(selected) >= 1 and itm not in selected))
                 for itm in items],
                spacing=8, run_spacing=8,wrap=True
            ),
            ft.Container(height=12),
        ])

    # ------------------------------------------------------------------
    def _badge(self, text, selected, on_click, disabled=False):
        # --- FIX 6: Removed debug print ---
        return ft.Container(
            content=ft.Row([ft.Text(text, size=13), ft.Icon(ft.Icons.CHECK, size=14, visible=selected)], spacing=4, tight=True),
            padding=ft.padding.symmetric(12, 6),
            bgcolor=ft.Colors.INDIGO_600 if selected else ft.Colors.TRANSPARENT,
            border=ft.border.all(1, ft.Colors.INDIGO_600 if selected else ft.Colors.GREY_400),
            border_radius=20,
            on_click=on_click if not disabled else None,
            opacity=0.5 if disabled else 1.0,
        )

    # ------------------------------------------------------------------
    def _toggle_skill(self, skill):
        # --- FIX 4: Cleanup debug print ---
        # print(f"TOGGLE SKILL: {skill}")
        if skill in self.skills:
            self.skills.remove(skill)
        elif len(self.skills) < 3:
            self.skills.append(skill)
        self._update_generate_button()
        self._refresh_all_sections()
        self.page.update()

    def _toggle_major(self, major):
        # --- FIX 4: Cleanup debug print ---
        # print(f"TOGGLE MAJOR: {major}")
        if major in self.major:
            self.major.clear()
        else:
            self.major = [major]
        self._update_generate_button()
        self._refresh_all_sections()
        self.page.update()

    def _toggle_interest(self, interest):
        # --- FIX 4: Cleanup debug print ---
        # print(f"TOGGLE INTEREST: {interest}")
        if interest in self.interests:
            self.interests.remove(interest)
        elif len(self.interests) < 3:
            self.interests.append(interest)
        self._refresh_all_sections()
        self._update_generate_button()
        self.page.update()
        
    def _refresh_all_sections(self):
        # --- FIX 5: Removed debug print ---
        self.skills_section.content = self._section("Skills", skills, self.skills, 3, self._toggle_skill)
        self.major_section.content = self._section("Major (choose 1)", major, self.major, 1, self._toggle_major, True)
        self.interests_section.content = self._section("Interests", interests, self.interests, 3, self._toggle_interest)

        # --- FIX 3: Removed redundant page update ---
        # self.page.update() 
    
    # ------------------------------------------------------------------
    def _update_generate_button(self):
        ready = len(self.skills) == 3 and len(self.major) == 1 and len(self.interests) == 3
        self.gen_btn.disabled = not ready
        # The page.update() in the toggle methods will update the button state

    def _generate(self, _):
        path = {
            "name": f"{self.major[0]} – {', '.join(self.skills)}",
            "description": f"Skills: {', '.join(self.skills)} | Interests: {', '.join(self.interests)}",
            "projects": [{"id": f"p{i}", "title": f"Project {i}", "prerequisite": f"p{i-1}" if i > 1 else None} for i in range(1, 6)]
        }
        major = self.major[0]
        us = UserInfo.UserInfo(self.skills,major,self.interests,"Laptop",1000,["Learning Machine"])
        self.on_path_generated(us)
        self.close()

    # ------------------------------------------------------------------
    def show(self):
        self.page.overlay.append(self.overlay)
        self.page.update()

    def close(self):
        if self.overlay in self.page.overlay:
            self.page.overlay.remove(self.overlay)
        
        # --- FIX 2: Call the on_close callback ---
        
        self.page.update()
