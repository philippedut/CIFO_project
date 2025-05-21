import numpy as np

from Team import Team


NUM_TEAMS = 5

class League:
    """Class to represent the entire league (a solution)"""
    def __init__(self, num_teams=NUM_TEAMS):
        self.teams = [Team(i) for i in range(num_teams)]
    
    def get_avg_skills(self):
        return [team.get_avg_skill() for team in self.teams]
    
    def get_skill_std_dev(self):
        avg_skills = self.get_avg_skills()
        return np.std(avg_skills)
    
    def is_valid(self):
        """Check if the league configuration is valid"""
        # Check if all teams have valid formations and are within budget
        for team in self.teams:
            if not team.has_valid_formation() or not team.is_within_budget():
                return False
        
        # Check if all players are assigned exactly once (would need player list)
        # This is handled implicitly by the algorithm
        
        return True
    
    def __str__(self):
        result = f"League (Skill StdDev: {self.get_skill_std_dev():.4f}):\n"
        for team in self.teams:
            result += f"{team}\n"
        return result
