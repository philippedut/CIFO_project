import random

from League import League 

NUM_TEAMS = 5

class MutationMethods:
    """Class containing different mutation methods for the genetic algorithm"""
    
    @staticmethod
    def swap_mutation(league, mutation_rate=0.2):
        """
        Mutate a league by swapping players of the same position between two random teams
        """
        # Don't always mutate
        if random.random() > mutation_rate:
            return league
        
        # Make a deep copy of the league to avoid modifying the original
        mutated = League()
        for i, team in enumerate(league.teams):
            for player in team.players:
                mutated.teams[i].add_player(player)
        
        # Randomly select two teams
        team_idx1 = random.randint(0, NUM_TEAMS - 1)
        team_idx2 = random.randint(0, NUM_TEAMS - 1)
        
        # Make sure teams are different
        while team_idx1 == team_idx2:
            team_idx2 = random.randint(0, NUM_TEAMS - 1)
        
        # Randomly select a position to swap
        pos = random.choice(['GK', 'DEF', 'MID', 'FWD'])
        
        # Get players of the selected position from both teams
        team1_players = [p for p in mutated.teams[team_idx1].players if p.position == pos]
        team2_players = [p for p in mutated.teams[team_idx2].players if p.position == pos]
        
        # If either team doesn't have players of this position, don't mutate
        if not team1_players or not team2_players:
            return league
        
        # Select a random player from each team
        player1 = random.choice(team1_players)
        player2 = random.choice(team2_players)
        
        # Swap the players
        # First, remove the players from their teams
        mutated.teams[team_idx1].players.remove(player1)
        mutated.teams[team_idx2].players.remove(player2)
        
        # Then, add them to the opposite teams
        mutated.teams[team_idx1].add_player(player2)
        mutated.teams[team_idx2].add_player(player1)
        
        return mutated
    
    @staticmethod
    def position_shuffle_mutation(league, mutation_rate=0.15):
        """
        Mutate a league by shuffling all players of a randomly selected position
        """
        # Don't always mutate
        if random.random() > mutation_rate:
            return league
        
        # Make a deep copy of the league to avoid modifying the original
        mutated = League()
        for i, team in enumerate(league.teams):
            for player in team.players:
                mutated.teams[i].add_player(player)
        
        # Randomly select a position to shuffle
        pos = random.choice(['GK', 'DEF', 'MID', 'FWD'])
        
        # Collect all players of this position
        all_pos_players = []
        for team in mutated.teams:
            for player in team.players[:]:
                if player.position == pos:
                    all_pos_players.append(player)
                    team.players.remove(player)
        
        # Shuffle these players
        random.shuffle(all_pos_players)
        
        # Reassign players to teams
        for i, team in enumerate(mutated.teams):
            if pos == 'GK':
                # Each team gets 1 GK
                if i < len(all_pos_players):
                    team.add_player(all_pos_players[i])
            else:
                # Each team gets 2 players for other positions
                start_idx = i * 2
                for j in range(2):
                    idx = start_idx + j
                    if idx < len(all_pos_players):
                        team.add_player(all_pos_players[idx])
        
        return mutated
    
    @staticmethod
    def scramble_mutation(league, mutation_rate=0.1):
        """
        Mutate a league by scrambling players within a randomly selected team
        """
        # Don't always mutate
        if random.random() > mutation_rate:
            return league
        
        # Make a deep copy of the league to avoid modifying the original
        mutated = League()
        for i, team in enumerate(league.teams):
            for player in team.players:
                mutated.teams[i].add_player(player)
        
        # Randomly select a team to scramble
        team_idx = random.randint(0, NUM_TEAMS - 1)
        
        # Group players by position (we need to maintain position constraints)
        gk_players = [p for p in mutated.teams[team_idx].players if p.position == 'GK']
        def_players = [p for p in mutated.teams[team_idx].players if p.position == 'DEF']
        mid_players = [p for p in mutated.teams[team_idx].players if p.position == 'MID']
        fwd_players = [p for p in mutated.teams[team_idx].players if p.position == 'FWD']
        
        # Since we can't swap players between positions, we'll just scramble within each position group
        # For GK, there's only one, so no scrambling
        # For other positions, we can swap players within the team
        
        # Scramble DEF
        if len(def_players) >= 2:
            for i in range(len(def_players)):
                swap_idx = random.randint(0, len(def_players) - 1)
                # Check if we can swap with another team
                if random.random() < 0.5:
                    # Randomly select another team
                    other_team_idx = random.randint(0, NUM_TEAMS - 1)
                    while other_team_idx == team_idx:
                        other_team_idx = random.randint(0, NUM_TEAMS - 1)
                    
                    # Get DEF players from the other team
                    other_defs = [p for p in mutated.teams[other_team_idx].players if p.position == 'DEF']
                    if other_defs:
                        # Swap with a random DEF from the other team
                        other_def = random.choice(other_defs)
                        mutated.teams[other_team_idx].players.remove(other_def)
                        mutated.teams[team_idx].players.remove(def_players[i])
                        
                        mutated.teams[other_team_idx].add_player(def_players[i])
                        mutated.teams[team_idx].add_player(other_def)
        
        # Similar scrambling for MID and FWD can be implemented here
        
        return mutated