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

        self.skills: List[str] = []
        self.major: List[str] = []
        self.interests: List[str] = []

        self.skills_search = ""
        self.skills_visible_items = 10
        self.major_search = ""
        self.major_visible_items = 10
        self.interests_search = ""
        self.interests_visible_items = 10

        self.skills_section = ft.Container()
        self.major_section = ft.Container()
        self.interests_section = ft.Container()
        # ----------------------------------------

        title = ft.Row([
            ft.Icon(ft.Icons.AUTO_AWESOME, color=ft.Colors.CYAN_400, size=28),
            ft.Text("Create Your Learning Path", weight=ft.FontWeight.BOLD, size=22, color=ft.Colors.WHITE)
        ], spacing=12)

        self.gen_btn = ft.FilledButton(
            "Generate Path",
            icon=ft.Icons.STARS,
            on_click=self._generate,
            expand=True,
            style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_400, color=ft.Colors.BLACK),
        )
        self.can_btn = ft.OutlinedButton(
            "Cancel", on_click=lambda _: self.close(), expand=True
        )
        self._content = ft.Container(
            ft.Column([
                title,
                ft.Container(height=10),
                ft.Text("Select your skills, major, and interests to generate a personalized learning path.", color=ft.Colors.GREY_400),
                ft.Container(height=20),
                self.skills_section,
                self.major_section,
                self.interests_section,
                # -------------------------------------------------

                ft.Container(height=30),
                ft.Row([self.gen_btn, self.can_btn], spacing=12),
            ], scroll=ft.ScrollMode.AUTO),
            width=620,
            padding=24,
            bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.GREY_900),
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=30, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK)),
        )
        self.backdrop:ft.Container = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
            expand=True,
            on_click=lambda _: self.close(),
        )

        self.overlay:ft.Stack = ft.Stack([
            self.backdrop,
            ft.Container(self._content, alignment=ft.alignment.center),
        ])

        self._refresh_all_sections()
        self._update_generate_button()

    # ------------------------------------------------------------------
    def _section(self, title, all_items, selected, max_allowed, toggle_cb, search_query, visible_items, on_search, on_show_more, on_show_less, single_select=False):
        filtered_items = [item for item in all_items if search_query.lower() in item.lower()]
        visible_items_list = filtered_items[:visible_items]

        search_bar = ft.TextField(
            label=f"Search {title}",
            value=search_query,
            on_submit=lambda e: on_search(e.control.value),
            dense=True,
            height=45,
            prefix_icon=ft.Icons.SEARCH,
            border_radius=20,
        )

        show_more_button = ft.TextButton(
            "Show More",
            icon=ft.Icons.ARROW_DOWNWARD,
            on_click=lambda _: on_show_more(),
            visible=len(filtered_items) > visible_items,
        )

        show_less_button = ft.TextButton(
            "Show Less",
            icon=ft.Icons.ARROW_UPWARD,
            on_click=lambda _: on_show_less(),
            visible=visible_items > 10,
        )

        return ft.Column([
            ft.Divider(height=1, color=ft.Colors.GREY_800),
            ft.Container(height=10),
            ft.Row([
                ft.Text(f"{title}", weight=ft.FontWeight.BOLD, size=16),
                ft.Text(f"({len(selected)}/{max_allowed})", size=12, color=ft.Colors.GREY_500)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=5),
            search_bar,
            ft.Container(height=15),
            ft.Row(
                [self._badge(itm, itm in selected, lambda _, s=itm: toggle_cb(s),
                            disabled=(len(selected) >= max_allowed and itm not in selected) or
                                     (single_select and len(selected) >= 1 and itm not in selected))
                 for itm in visible_items_list],
                spacing=10, run_spacing=10, wrap=True
            ),
            ft.Row([show_more_button, show_less_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
        ])

    # ------------------------------------------------------------------
    def _badge(self, text, selected, on_click, disabled=False):
        return ft.Container(
            content=ft.Row([ft.Text(text, size=13,color=ft.Colors.WHITE, weight=ft.FontWeight.NORMAL), ft.Icon(ft.Icons.CHECK_CIRCLE, size=14, visible=selected, color=ft.Colors.WHITE)], spacing=4, tight=True),
            padding=ft.padding.symmetric(12, 8),
            bgcolor=ft.Colors.CYAN_800 if selected else ft.Colors.with_opacity(0.3, ft.Colors.WHITE10),
            border=ft.border.all(1, ft.Colors.CYAN_700 if selected else ft.Colors.WHITE24),
            border_radius=20,
            on_click=on_click if not disabled else None,
            opacity=0.6 if disabled else 1.0,
            animate=ft.Animation(200, "easeOut"),
            on_hover=self._on_badge_hover,
        )

    def _on_badge_hover(self, e):
        is_selected = e.control.content.controls[1].visible
        if e.data == "true":
            e.control.bgcolor = ft.Colors.with_opacity(0.5, ft.Colors.WHITE10)
        else:
            e.control.bgcolor = ft.Colors.CYAN_800 if is_selected else ft.Colors.with_opacity(0.3, ft.Colors.WHITE10)
        e.control.update()

    # ------------------------------------------------------------------
    def _toggle_skill(self, skill):
        if skill in self.skills:
            self.skills.remove(skill)
        elif len(self.skills) < 3:
            self.skills.append(skill)
        self._update_generate_button()
        self._refresh_all_sections()
        self.page.update()

    def _toggle_major(self, major_item):
        if major_item in self.major:
            self.major.clear()
        else:
            self.major = [major_item]
        self._update_generate_button()
        self._refresh_all_sections()
        self.page.update()

    def _toggle_interest(self, interest):
        if interest in self.interests:
            self.interests.remove(interest)
        elif len(self.interests) < 3:
            self.interests.append(interest)
        self._refresh_all_sections()
        self._update_generate_button()
        self.page.update()

    def _on_skills_search(self, query):
        self.skills_search = query
        self.skills_visible_items = 10
        self._refresh_all_sections()
        self.page.update()

    def _on_skills_show_more(self):
        self.skills_visible_items += 10
        self._refresh_all_sections()
        self.page.update()

    def _on_skills_show_less(self):
        self.skills_visible_items = 10
        self._refresh_all_sections()
        self.page.update()

    def _on_major_search(self, query):
        self.major_search = query
        self.major_visible_items = 10
        self._refresh_all_sections()
        self.page.update()

    def _on_major_show_more(self):
        self.major_visible_items += 10
        self._refresh_all_sections()
        self.page.update()

    def _on_major_show_less(self):
        self.major_visible_items = 10
        self._refresh_all_sections()
        self.page.update()

    def _on_interests_search(self, query):
        self.interests_search = query
        self.interests_visible_items = 10
        self._refresh_all_sections()
        self.page.update()

    def _on_interests_show_more(self):
        self.interests_visible_items += 10
        self._refresh_all_sections()
        self.page.update()

    def _on_interests_show_less(self):
        self.interests_visible_items = 10
        self._refresh_all_sections()
        self.page.update()
        
    def _refresh_all_sections(self):
        self.skills_section.content = self._section(
            "Skills", skills, self.skills, 3, self._toggle_skill,
            self.skills_search, self.skills_visible_items,
            self._on_skills_search, self._on_skills_show_more, self._on_skills_show_less
        )
        self.major_section.content = self._section(
            "Major (choose 1)", major, self.major, 1, self._toggle_major,
            self.major_search, self.major_visible_items,
            self._on_major_search, self._on_major_show_more, self._on_major_show_less, True
        )
        self.interests_section.content = self._section(
            "Interests", interests, self.interests, 3, self._toggle_interest,
            self.interests_search, self.interests_visible_items,
            self._on_interests_search, self._on_interests_show_more, self._on_interests_show_less
        )

    
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
