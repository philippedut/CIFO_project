import random

from League import League 

NUM_TEAMS = 5


class CrossoverMethods:
    """Class containing different crossover methods for the genetic algorithm"""
    
    @staticmethod
    def team_based_crossover(parent1, parent2, player_count):
        """
        Create offspring using team-based crossover
        
        This crossover:
        1. For each team position, randomly selects the team from either parent1 or parent2
        2. Checks if the resulting league is valid (no duplicate players)
        """
        child = League()
        
        # For each team position, randomly choose the team from either parent1 or parent2
        for i in range(NUM_TEAMS):
            if random.random() < 0.5:
                # Take team from parent1
                for player in parent1.teams[i].players:
                    child.teams[i].add_player(player)
            else:
                # Take team from parent2
                for player in parent2.teams[i].players:
                    child.teams[i].add_player(player)
        
        # Check if child is valid (no duplicate players, etc.)
        player_ids = set()
        for team in child.teams:
            for player in team.players:
                if player.id in player_ids:
                    # Found a duplicate player, signal invalid child
                    return None
                player_ids.add(player.id)
        
        # Make sure we have all players assigned
        if len(player_ids) != player_count:
            return None
        
        return child
    
    @staticmethod
    def position_based_crossover(parent1, parent2, player_count):
        """
        Create offspring using position-based crossover
        
        This crossover:
        1. Randomly selects which parent to take players from for each position type
        2. For example, might take GKs from parent1, DEFs from parent2, etc.
        """
        child = League()
        
        # Track assigned players to avoid duplicates
        assigned_players = set()
        
        # For each position type, choose which parent to take players from
        for position in ['GK', 'DEF', 'MID', 'FWD']:
            # Randomly select parent for this position
            source_parent = parent1 if random.random() < 0.5 else parent2
            
            # Get all players of this position from the source parent
            position_players = []
            for team in source_parent.teams:
                for player in team.players:
                    if player.position == position:
                        position_players.append((team.id, player))
            
            # Assign these players to the same teams in the child
            for team_id, player in position_players:
                if player.id not in assigned_players:
                    child.teams[team_id].add_player(player)
                    assigned_players.add(player.id)
        
        # Check if we have any missing positions
        valid_formation = True
        for team in child.teams:
            if not team.has_valid_formation():
                valid_formation = False
                break
        
        # If the formation is invalid or we have missing players, signal invalid child
        if not valid_formation or len(assigned_players) != player_count:
            return None
        
        return child

