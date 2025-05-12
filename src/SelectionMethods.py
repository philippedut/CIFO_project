import random

class SelectionMethods:
    """Class containing different selection methods for the genetic algorithm"""
    
    @staticmethod
    def tournament_selection(population, fitness_func, tournament_size=3):
        """
        Select an individual using tournament selection
        
        Based on section 3.1.3 of the textbook, tournament selection:
        1. Randomly selects k individuals
        2. Returns the best one among them
        """
        # Randomly select tournament_size individuals
        tournament = random.sample(population, tournament_size)
        
        # Return the best individual from the tournament
        return min(tournament, key=fitness_func)
    
    @staticmethod
    def roulette_wheel_selection(population, fitness_func):
        """
        Select an individual using roulette wheel (fitness proportionate) selection
        
        Based on section 3.1.1 of the textbook, roulette wheel selection:
        1. Assigns selection probability proportional to fitness
        2. For minimization problems, we need to transform fitness values
        """
        # Get fitness values for all individuals
        fitnesses = [fitness_func(individual) for individual in population]
        
        # Since we're minimizing, we need to transform fitness values
        # We'll use the reciprocal of fitness, but add a small value to avoid division by zero
        transformed_fitnesses = [1.0 / (f + 0.01) for f in fitnesses]
        
        # Normalize to get probabilities
        total_fitness = sum(transformed_fitnesses)
        probabilities = [f / total_fitness for f in transformed_fitnesses]
        
        # Select using roulette wheel (cumulative probability)
        r = random.random()
        cumulative_prob = 0
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if r <= cumulative_prob:
                return population[i]
        
        # Fallback (shouldn't reach here normally)
        return random.choice(population)
