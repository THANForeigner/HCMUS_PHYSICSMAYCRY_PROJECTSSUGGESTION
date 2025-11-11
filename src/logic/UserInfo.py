class UserInfo:
    def __init__(self, skills: list[str], major: str, interests: list[str], material: str, weekly_hours: int, goals: list[str]):
        self.skills = skills
        self.major = major
        self.interests = interests
        self.material = material
        self.weekly_hours = weekly_hours
        self.goals =  goals
        self.past_suggestions = []
    
    def to_dict(self):
        return {
            "Skills": self.skills,
            "Major": self.major,
            "Interests": self.interests,
            "Material": self.material,
            "Weekly_hours": self.weekly_hours,
            "Goals": self.goals
        }