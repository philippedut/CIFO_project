class Player:
    """Class to represent a player"""
    def __init__(self, id, name, position, skill, salary):
        self.id = id
        self.name = name
        self.position = position
        self.skill = skill
        self.salary = salary
    
    def __str__(self):
        return f"{self.name} ({self.position}, Skill={self.skill}, Salary={self.salary}M€)"
