class Team(BUDGET_LIMIT=750):
    #BUDGET_LIMIT = 750  # in million €
    """Class to represent a team"""
    def __init__(self, team_id):
        self.id = team_id
        self.players = []
        self.budget_limit = Team.BUDGET_LIMIT
    
    def add_player(self, player):
        self.players.append(player)
    
    def get_total_salary(self):
        return sum(player.salary for player in self.players)
    
    def get_avg_skill(self):
        if not self.players:
            return 0
        return sum(player.skill for player in self.players) / len(self.players)
    
    def is_within_budget(self):
        return self.get_total_salary() <= self.budget_limit
    
    def has_valid_formation(self):
        # Check if the team has exactly 1 GK, 2 DEF, 2 MID, and 2 FWD
        pos_count = {'GK': 0, 'DEF': 0, 'MID': 0, 'FWD': 0}
        for player in self.players:
            pos_count[player.position] = pos_count.get(player.position, 0) + 1
        
        return pos_count.get('GK', 0) == 1 and pos_count.get('DEF', 0) == 2 and \
               pos_count.get('MID', 0) == 2 and pos_count.get('FWD', 0) == 2
    
    def __str__(self):
        result = f"Team {self.id+1} (Avg Skill: {self.get_avg_skill():.2f}, Salary: {self.get_total_salary()}M€):\n"
        # Sort players by position
        sorted_players = sorted(self.players, key=lambda p: p.position)
        for player in sorted_players:
            result += f"  - {player}\n"
        return result

