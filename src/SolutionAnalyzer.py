import pandas as pd 

# Define the budget limit constant
BUDGET_LIMIT = 750  



class SolutionAnalyzer:
    """Class for analyzing and exporting the solutions"""
    
    @staticmethod
    def analyze_solution(league):
        """Analyze and print detailed information about the solution"""
        print("\n" + "="*50)
        print("FANTASY LEAGUE SOLUTION ANALYSIS")
        print("="*50)
        
        # Print league information
        print(f"\nLeague Standard Deviation: {league.get_skill_std_dev():.4f}")
        print(f"League Valid: {league.is_valid()}")
        
        # Print team details
        print("\nTEAM DETAILS:")
        for i, team in enumerate(league.teams):
            print(f"\nTeam {i+1}:")
            print(f"  Average Skill: {team.get_avg_skill():.2f}")
            print(f"  Total Salary: {team.get_total_salary()}M€ (Limit: {BUDGET_LIMIT}M€)")
            print(f"  Valid Formation: {team.has_valid_formation()}")
            print(f"  Within Budget: {team.is_within_budget()}")
            print("  Players:")
            
            # Group and print players by position
            for pos in ['GK', 'DEF', 'MID', 'FWD']:
                pos_players = [p for p in team.players if p.position == pos]
                print(f"    {pos}:")
                for player in pos_players:
                    print(f"      - {player.name} (Skill: {player.skill}, Salary: {player.salary}M€)")
        
        print("\n" + "="*50)
    
    @staticmethod
    def export_solution_to_csv(league, filename):
        """Export the league solution to a CSV file"""
        data = []
        for team_idx, team in enumerate(league.teams):
            for player in team.players:
                data.append({
                    'Team': f'Team {team_idx+1}',
                    'PlayerID': player.id,
                    'Name': player.name,
                    'Position': player.position,
                    'Skill': player.skill,
                    'Salary': player.salary
                })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Solution exported to {filename}")