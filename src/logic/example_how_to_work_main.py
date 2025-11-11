from logic.Suggestion import Suggestion
from logic.UserInfo import UserInfo
import os
def example_main():
    print(os.getcwd())
    user = UserInfo(
        skills=["Python", "Data Analysis"],
        major="Computer Science",
        interests=["Machine Learning", "AI"],
        material="Laptop",
        weekly_hours=10,
        goals=["Learn ML", "Build Projects"]
    )

    suggester = Suggestion()
    suggested_projects = suggester.ProjectSuggestList(user)

    print("Top Suggested Projects:")
    for project in suggested_projects:
        print(f"- {project.title}: {project.description}")
        
