from Suggestion import Suggestion
from UserInfo import UserInfo
def example_main():
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
        
#if __name__ == "__main__":
#    main()