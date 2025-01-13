import numpy as np
import random

# Fitness Function
def fitness(individual):
    score = 0
    for i in range(9):
        score += len(set(individual[i]))  # Row uniqueness
        score += len(set(individual[:, i]))  # Column uniqueness
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            subgrid = individual[row:row+3, col:col+3].flatten()
            score += len(set(subgrid))  # Subgrid uniqueness
    return score - (243 - score)  # Penalize for duplicates

# Generate Initial Population
def generate_population(puzzle, size=100):
    population = []
    for _ in range(size):
        individual = puzzle.copy()
        for row in range(9):
            empty_indices = [i for i in range(9) if individual[row, i] == 0]
            missing_values = list(set(range(1, 10)) - set(individual[row]))
            random.shuffle(missing_values)
            for idx, value in zip(empty_indices, missing_values):
                individual[row, idx] = value
        population.append(individual)
    return population

# Crossover Function
def crossover(parent1, parent2):
    child = parent1.copy()
    for row in range(9):
        if random.random() > 0.5:
            child[row] = parent2[row]
    return child

# Mutation Function
def mutate(individual, puzzle, mutation_rate=0.1):
    for row in range(9):
        if random.random() < mutation_rate:
            mutable_indices = [i for i in range(9) if puzzle[row, i] == 0]
            if len(mutable_indices) > 1:
                idx1, idx2 = random.sample(mutable_indices, 2)
                individual[row, idx1], individual[row, idx2] = individual[row, idx2], individual[row, idx1]
    return individual

# Roulette Selection
def roulette_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    selection_probs = [f / total_fitness for f in fitness_scores]
    selected_index = np.random.choice(len(population), p=selection_probs)
    return population[selected_index]

# Tournament Selection
def tournament_selection(population, fitness_scores, k=5):
    tournament_indices = random.sample(range(len(population)), k)
    tournament_individuals = [population[i] for i in tournament_indices]
    tournament_fitness = [fitness_scores[i] for i in tournament_indices]
    winner_index = tournament_fitness.index(max(tournament_fitness))
    return tournament_individuals[winner_index]

# Genetic Algorithm
def genetic_algorithm(puzzle, generations=2000, population_size=170, mutation_rate=0.25, elite_fraction=0.25, selection_type="roulette"):
    population = generate_population(puzzle, population_size)

    for generation in range(generations):
        fitness_scores = [fitness(ind) for ind in population]

        if max(fitness_scores) == 243:  # Perfect solution
            return population[fitness_scores.index(max(fitness_scores))], generation

        elite_count = int(elite_fraction * population_size)
        elites = [population[i] for i in np.argsort(fitness_scores)[-elite_count:]]

        if selection_type == "roulette":
            parents = [roulette_selection(population, fitness_scores) for _ in range(population_size - elite_count)]
        elif selection_type == "tournament":
            parents = [tournament_selection(population, fitness_scores, k=5) for _ in range(population_size - elite_count)]
        else:
            raise ValueError("Invalid selection type. Choose 'roulette' or 'tournament'.")

        new_population = elites + [
            mutate(crossover(random.choice(parents), random.choice(parents)), puzzle, mutation_rate)
            for _ in range(population_size - elite_count)
        ]
        population = new_population

    return max(population, key=fitness), generations  # Best candidate if no solution

# Backtracking Refinement
def backtrack(grid):
    def is_valid(grid, row, col, num):
        if num in grid[row] or num in grid[:, col]:
            return False
        subgrid = grid[row//3*3:row//3*3+3, col//3*3:col//3*3+3]
        return num not in subgrid.flatten()

    for row in range(9):
        for col in range(9):
            if grid[row, col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row, col] = num
                        if backtrack(grid):
                            return True
                        grid[row, col] = 0
                return False
    return True

"""
Console Debug:
print("Generating Sudoku puzzle...")
puzzle = sg.generate_sudoku(difficulty="easy")
print("Puzzle Generated:")
print(puzzle)
print("Running genetic algorithm...")
solution = genetic_algorithm(puzzle)

print("Best candidate solution:")
print(solution)

if is_valid_solution(solution):
    print("Valid solution found!")
else:
    print("Refining with backtracking...")
    if backtrack(solution):
        print("Final solution:")
        print(solution)
    else:
        print("Backtracking failed.") """