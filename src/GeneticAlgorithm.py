import random
import time
import matplotlib.pyplot as plt
from League import League
from CrossoverMethods import CrossoverMethods
from SelectionMethods import SelectionMethods
from MutationMethods import MutationMethods
import matplotlib.pyplot as plt

BUDGET_LIMIT = 750

class BaseGeneticAlgorithm:
    """Generic GA template; subclasses define selection, crossover, mutation."""
    NUM_TEAMS = 5

    def __init__(self, players, pop_size=40, generations=100):
        self.players = players
        self.pop_size = pop_size
        self.generations = generations
        self.population = []
        self.best_solution = None
        self.best_fitness = float('inf')
        self.fitness_history = []
        # Group players by position
        self.players_by_pos = {
            'GK': [p for p in players if p.position == 'GK'],
            'DEF': [p for p in players if p.position == 'DEF'],
            'MID': [p for p in players if p.position == 'MID'],
            'FWD': [p for p in players if p.position == 'FWD']
        }

    def create_random_individual(self):
        """Creates a random team by selecting players from the available pool.
        It ensures that the team has a valid formation and does not exceed the budget limit."""
        league = League()
        gks = self.players_by_pos['GK'].copy()
        defs = self.players_by_pos['DEF'].copy()
        mids = self.players_by_pos['MID'].copy()
        fwds = self.players_by_pos['FWD'].copy()
        random.shuffle(gks); random.shuffle(defs)
        random.shuffle(mids); random.shuffle(fwds)
        for i in range(self.NUM_TEAMS):
            if i < len(gks): league.teams[i].add_player(gks[i])
            for j in range(2):
                idx = i*2 + j
                if idx < len(defs): league.teams[i].add_player(defs[idx])
                if idx < len(mids): league.teams[i].add_player(mids[idx])
                if idx < len(fwds): league.teams[i].add_player(fwds[idx])
        return league

    def initialize_population(self):
        self.population = [self.create_random_individual() for _ in range(self.pop_size)]

    def fitness(self, league):
        """Calculates the fitness of a league based on the standard deviation of team skills."""
        for team in league.teams:
            if not team.has_valid_formation():
                return 1000.0
            if team.get_total_salary() > BUDGET_LIMIT:
                return 500.0 + (team.get_total_salary() - BUDGET_LIMIT)
        return league.get_skill_std_dev()
   

    def run(self):
        print("Starting genetic algorithm...")
        
        # Record the start time to measure elapsed execution time later
        start_time = time.time()
        
        # Initialize the population with random individuals
        print("Initializing population...")
        self.initialize_population()
        
        # Evaluate the fitness of the initial population
        for ind in self.population:
            fit = self.fitness(ind)
            # If this individual is the best seen so far, update the best records
            if fit < self.best_fitness:
                self.best_fitness = fit
                self.best_solution = ind

        # Store the best fitness of the initial population
        self.fitness_history.append(self.best_fitness)
        print(f"Initial best fitness: {self.best_fitness:.4f}")

        # Begin the evolution process across a fixed number of generations
        for gen in range(self.generations):
            # Create a new population starting with the current best individual (elitism)
            new_pop = [self.best_solution]

            # Fill the rest of the new population
            while len(new_pop) < self.pop_size:
                # Select two parents using the selection method
                parent1 = self.selection(self.population, self.fitness)
                parent2 = self.selection(self.population, self.fitness)
                
                # Retry selection if both parents are the same (to maintain diversity)
                retry = 0
                while parent1 is parent2 and retry < 5:
                    parent2 = self.selection(self.population, self.fitness)
                    retry += 1

                # Perform crossover to produce offspring
                offspring = self.crossover(parent1, parent2, len(self.players))

                # If crossover fails (e.g., returns None), fall back to a random individual
                if offspring is None:
                    offspring = self.create_random_individual()

                # Apply mutation to the offspring
                offspring = self.mutation(offspring)

                # Add the resulting offspring to the new population
                new_pop.append(offspring)

            # Replace the current population with the new one
            self.population = new_pop

            # Evaluate the fitness of the new population
            for ind in self.population:
                fit = self.fitness(ind)
                # Update best fitness and solution if a better one is found
                if fit < self.best_fitness:
                    self.best_fitness = fit
                    self.best_solution = ind

            # Log the best fitness of the current generation
            self.fitness_history.append(self.best_fitness)

            # Every 10 generations (or final generation), print progress and time
            if gen % 10 == 0 or gen == self.generations - 1:
                elapsed = time.time() - start_time
                print(f"Generation {gen}: Best fitness = {self.best_fitness:.4f} (Time: {elapsed:.2f}s)")

        # Print summary once the algorithm completes
        print(f"Evolution completed in {time.time() - start_time:.2f} seconds")
        print(f"Final best fitness: {self.best_fitness:.4f}")

        # Return the best solution and fitness progression over time
        return self.best_solution, self.fitness_history

    def get_fitness_history(self):
        return self.fitness_history

    # Plot the fitness history over generations
    def plot_fitness_history(self):
        plt.figure(figsize=(10,6))
        plt.plot(self.fitness_history)
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness (StdDev)')
        plt.title('Best Fitness per Generation')
        plt.grid(True)
        plt.show()

# Define subclasses for all combinations
_selections = {
    'tournament': SelectionMethods.tournament_selection,
    'roulette_wheel': SelectionMethods.roulette_wheel_selection
}
_crossovers = {
    'team': CrossoverMethods.team_based_crossover,
    'positionbased': CrossoverMethods.position_based_crossover
}
_mutations = {
    'swap': MutationMethods.swap_mutation,
    'positionshuffle': MutationMethods.position_shuffle_mutation,
    'scramble': MutationMethods.scramble_mutation
}

#Generate subclasses for all combinations of selection, crossover, and mutation methods. 
#This is done to create a unique class for each combination, allowing for easy instantiation and usage of different genetic algorithm configurations.
for sel_name, sel_fn in _selections.items():
    for mut_name, mut_fn in _mutations.items():
        for cross_name, cross_fn in _crossovers.items():
            cls_name = f"GeneticAlgorithm_{sel_name}_{mut_name}_{cross_name}"
            globals()[cls_name] = type(
                cls_name,
                (BaseGeneticAlgorithm,),
                {
                    'selection': staticmethod(sel_fn),
                    'crossover': staticmethod(cross_fn),
                    'mutation': staticmethod(mut_fn)
                }
            )