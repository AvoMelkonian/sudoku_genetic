import random

POPULATION_SIZE = 200  # Reduced population size
MUTATION_RATE = 0.2  # Lower mutation rate
GENERATIONS = 1000
TOURNAMENT_SIZE = 5  # Smaller tournament size for selection
ELITISM_COUNT = 10  # Elitism: keep the top N individuals unchanged
EARLY_STOPPING = 50  # Stop early if no improvement after 50 generations

# Initial puzzle (0 represents empty cells)
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

def get_fixed_cells(grid):
    """Identify fixed cells in the Sudoku grid."""
    return [[cell != 0 for cell in row] for row in grid]

def create_individual(grid, fixed_cells):
    """Generate a valid individual by filling empty cells."""
    individual = [row[:] for row in grid]
    for row in range(9):
        available_nums = list(set(range(1, 10)) - set(individual[row]))
        random.shuffle(available_nums)
        for col in range(9):
            if not fixed_cells[row][col]:  # Fill only mutable cells
                individual[row][col] = available_nums.pop()
    return individual

def create_population(grid, size, fixed_cells):
    """Create a population of Sudoku grids."""
    return [create_individual(grid, fixed_cells) for _ in range(size)]

def fitness_function(grid):
    """Compute the fitness of a Sudoku grid."""
    fitness = 0
    for row in grid:
        fitness += 9 - len(set(row))
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        fitness += 9 - len(set(column))
    for block_row in range(3):
        for block_col in range(3):
            block = [
                grid[r][c]
                for r in range(block_row * 3, block_row * 3 + 3)
                for c in range(block_col * 3, block_col * 3 + 3)
            ]
            fitness += 9 - len(set(block))
    return fitness

def is_valid_solution(grid):
    """Check if a Sudoku grid is valid."""
    return fitness_function(grid) == 0

def tournament_selection(population, tournament_size):
    """Select two parents using tournament selection."""
    selected = random.sample(population, tournament_size)
    selected.sort(key=fitness_function)
    return selected[0], selected[1]

def crossover(parent1, parent2, fixed_cells):
    """Perform crossover by combining rows from two parents."""
    offspring = []
    for row in range(9):
        offspring.append(parent1[row][:] if random.random() < 0.5 else parent2[row][:])
    return offspring

def mutate(individual, fixed_cells):
    """Mutate an individual by swapping non-fixed cells in a row."""
    for _ in range(2):
        row = random.randint(0, 8)
        mutable_indices = [col for col in range(9) if not fixed_cells[row][col]]
        if len(mutable_indices) > 1:
            i, j = random.sample(mutable_indices, 2)
            individual[row][i], individual[row][j] = individual[row][j], individual[row][i]

def genetic_algorithm(grid, generations, population_size, mutation_rate, tournament_size, elitism_count, early_stopping):
    """Solve Sudoku using a genetic algorithm."""
    fixed_cells = get_fixed_cells(grid)
    population = create_population(grid, population_size, fixed_cells)

    best_fitness = float('inf')
    stagnation_count = 0

    for generation in range(generations):
        # Tournament selection and evolution
        new_population = []
        population.sort(key=fitness_function)  # Sort for elitism
        new_population.extend(population[:elitism_count])  # Elitism: retain the best individuals

        while len(new_population) < population_size:
            parent1, parent2 = tournament_selection(population, tournament_size)
            offspring = crossover(parent1, parent2, fixed_cells)
            if random.random() < mutation_rate:
                mutate(offspring, fixed_cells)
            new_population.append(offspring)

        population = new_population

        # Check best fitness for early stopping
        current_best_fitness = fitness_function(population[0])
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            stagnation_count = 0
        else:
            stagnation_count += 1
        
        if stagnation_count >= early_stopping:
            print(f"Early stopping at generation {generation}")
            break

        # Stop if solution is found
        if best_fitness == 0:
            return population[0], generation

    return population[0], generations

def print_grid(grid):
    """Print a Sudoku grid."""
    for row in grid:
        print(row)

def main():
    print("Initial Puzzle:")
    print_grid(puzzle)

    solution, generations = genetic_algorithm(
        puzzle, GENERATIONS, POPULATION_SIZE, MUTATION_RATE, TOURNAMENT_SIZE, ELITISM_COUNT, EARLY_STOPPING
    )

    if is_valid_solution(solution):
        print(f"\nSolved Sudoku in {generations} generations:")
        print_grid(solution)
    else:
        print(f"\nBest Attempt after {generations} generations:")
        print_grid(solution)

if __name__ == "__main__":
    main()