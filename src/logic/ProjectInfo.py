class ProjectInfo:
    def __init__(self, Title:str, Description:str, Skills: list[str], Major:str, Interests: list[str], Required_material: list[str], Estimated_hours: int):
        self.title = Title
        self.description = Description
        self.skills = Skills
        self.major = Major
        self.interests = Interests
        self.required_material = Required_material
        self.estimated_hours = Estimated_hours

    def to_dict(self):
        return {
            "Title": self.title,
            "Description": self.description,
            "Skills": self.skills,
            "Major": self.major,
            "Interests": self.interests,
            "Required_material": self.required_material,
            "Estimated_hours": self.estimated_hours
        }