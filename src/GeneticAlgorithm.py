import random 
import time
# Visulization should be done in the main, not here
import matplotlib.pyplot as plt

# Custom classes 
from League import League
from CrossoverMethods import  CrossoverMethods
from SelectionMethods import SelectionMethods 
from MutationMethods import MutationMethods

BUDGET_LIMIT = 750 


class GeneticAlgorithm:
    """Implementation of a genetic algorithm to optimize the league"""
    def __init__(self, players, pop_size=40, generations=100):
        self.players = players
        self.pop_size = pop_size
        self.generations = generations
        self.population = []
        self.best_solution = None
        self.best_fitness = float('inf')  # We're minimizing
        self.fitness_history = []
        
        # Group players by position for easier access
        self.players_by_pos = {
            'GK': [p for p in players if p.position == 'GK'],
            'DEF': [p for p in players if p.position == 'DEF'],
            'MID': [p for p in players if p.position == 'MID'],
            'FWD': [p for p in players if p.position == 'FWD']
        }
    
    NUM_TEAMS = 5
    
    def create_random_individual(self):
        """Create a random valid league configuration"""
        league = League()
        
        # Shuffle players by position
        gks = self.players_by_pos['GK'].copy()
        defs = self.players_by_pos['DEF'].copy()
        mids = self.players_by_pos['MID'].copy()
        fwds = self.players_by_pos['FWD'].copy()
        
        random.shuffle(gks)
        random.shuffle(defs)
        random.shuffle(mids)
        random.shuffle(fwds)
        
        # Assign players to teams
        for i in range(GeneticAlgorithm.NUM_TEAMS):
            # Add 1 GK per team
            if i < len(gks):
                league.teams[i].add_player(gks[i])
            
            # Add 2 DEF per team
            for j in range(2):
                idx = i * 2 + j
                if idx < len(defs):
                    league.teams[i].add_player(defs[idx])
            
            # Add 2 MID per team
            for j in range(2):
                idx = i * 2 + j
                if idx < len(mids):
                    league.teams[i].add_player(mids[idx])
            
            # Add 2 FWD per team
            for j in range(2):
                idx = i * 2 + j
                if idx < len(fwds):
                    league.teams[i].add_player(fwds[idx])
        
        return league
    
    def initialize_population(self):
        """Initialize the population with random individuals"""
        self.population = []
        for _ in range(self.pop_size):
            individual = self.create_random_individual()
            self.population.append(individual)
    
    def fitness(self, league):
        """
        Calculate fitness for a league (lower is better)
        
        The fitness function evaluates:
        1. If formation is valid (1 GK, 2 DEF, 2 MID, 2 FWD per team)
        2. If all teams are within budget limit
        3. Standard deviation of average skills (our main objective)
        """
        # If the league is invalid, apply a penalty
        for team in league.teams:
            # Check formation
            if not team.has_valid_formation():
                return 1000.0
            
            # Check budget
            if team.get_total_salary() > BUDGET_LIMIT:
                return 500.0 + (team.get_total_salary() - BUDGET_LIMIT)
        
        # Calculate standard deviation of average skills (our objective function)
        # Lower standard deviation means more balanced league
        std_dev = league.get_skill_std_dev()
        
        # Add a small penalty for teams close to the budget limit
        budget_penalty = 0
        for team in league.teams:
            if team.get_total_salary() > 0.95 * BUDGET_LIMIT:
                budget_penalty += 0.00
        
        return std_dev + budget_penalty
    
    def run(self):
        """Run the genetic algorithm"""
        print("Starting genetic algorithm...")
        start_time = time.time()
        
        # Initialize population
        print("Initializing population...")
        self.initialize_population()
        
        # Evaluate initial population
        for individual in self.population:
            fitness = self.fitness(individual)
            if fitness < self.best_fitness:
                self.best_fitness = fitness
                self.best_solution = individual
        
        print(f"Initial best fitness: {self.best_fitness:.4f}")
        self.fitness_history.append(self.best_fitness)
        
        # Main evolution loop
        for generation in range(self.generations):
            # Create new population
            new_population = []
            
            # Elitism: keep the best individual
            new_population.append(self.best_solution)
            
            # Create the rest of the population through selection, crossover, mutation
            while len(new_population) < self.pop_size:
                # Selection - alternate between selection methods
                if len(new_population) % 2 == 0:
                    parent1 = SelectionMethods.tournament_selection(self.population, self.fitness)
                    parent2 = SelectionMethods.tournament_selection(self.population, self.fitness)
                else:
                    parent1 = SelectionMethods.roulette_wheel_selection(self.population, self.fitness)
                    parent2 = SelectionMethods.roulette_wheel_selection(self.population, self.fitness)
                
                # Make sure parents are different
                retry_count = 0
                while parent1 is parent2 and retry_count < 5:
                    parent2 = SelectionMethods.tournament_selection(self.population, self.fitness)
                    retry_count += 1
                
                # Crossover - alternate between crossover methods
                offspring = None
                if random.random() < 0.5:
                    offspring = CrossoverMethods.team_based_crossover(parent1, parent2, len(self.players))
                else:
                    offspring = CrossoverMethods.position_based_crossover(parent1, parent2, len(self.players))
                
                # If crossover produced an invalid offspring, create a random one
                if offspring is None:
                    offspring = self.create_random_individual()
                
                # Mutation - randomly select a mutation operator
                mutation_choice = random.random()
                if mutation_choice < 0.4:  # 40% chance
                    offspring = MutationMethods.swap_mutation(offspring)
                elif mutation_choice < 0.7:  # 30% chance
                    offspring = MutationMethods.position_shuffle_mutation(offspring)
                else:  # 30% chance
                    offspring = MutationMethods.scramble_mutation(offspring)
                
                # Add to new population
                new_population.append(offspring)
            
            # Replace old population
            self.population = new_population
            
            # Evaluate population and update best
            for individual in self.population:
                fitness = self.fitness(individual)
                if fitness < self.best_fitness:
                    self.best_fitness = fitness
                    self.best_solution = individual
            
            # Store best fitness for history
            self.fitness_history.append(self.best_fitness)
            
            # Print progress every 10 generations
            if generation % 10 == 0 or generation == self.generations - 1:
                elapsed = time.time() - start_time
                print(f"Generation {generation}: Best fitness = {self.best_fitness:.4f} (Time: {elapsed:.2f}s)")
        
        print(f"Evolution completed in {time.time() - start_time:.2f} seconds")
        print(f"Final best fitness: {self.best_fitness:.4f}")
        
        return self.best_solution
    
    def plot_fitness_history(self):
        """Plot the fitness history"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.fitness_history, 'b-')
        plt.xlabel('Generation')
        plt.ylabel('Fitness (StdDev) - Lower is better')
        plt.title('Fitness History')
        plt.grid(True)
        plt.savefig('fitness_history.png')
        plt.show()
