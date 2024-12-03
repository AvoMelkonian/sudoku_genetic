import random

POPULATION_SIZE = 500
MUTATION_RATE = 0.3
GENERATIONS = 2000

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

def create_individual(grid):
    """Generate a valid individual by filling empty cells while ensuring valid blocks and columns."""
    individual = [row[:] for row in grid]

    # Fill empty cells row by row
    for row in range(9):
        available_nums = list(set(range(1, 10)) - set(individual[row]))
        random.shuffle(available_nums)
        
        for col in range(9):
            if individual[row][col] == 0:
                valid_nums = [
                    num for num in available_nums
                    if num not in [individual[r][col] for r in range(9)]  # Column check
                    and num not in [
                        individual[r][c]
                        for r in range((row // 3) * 3, (row // 3) * 3 + 3)
                        for c in range((col // 3) * 3, (col // 3) * 3 + 3)
                    ]  # Block check
                ]
                if valid_nums:
                    selected = random.choice(valid_nums)
                    individual[row][col] = selected
                    available_nums.remove(selected)
    return individual

def create_population(grid, size):
    """Create a population of Sudoku grids."""
    return [create_individual(grid) for _ in range(size)]

def fitness_function(grid):
    """Compute the fitness of a Sudoku grid."""
    fitness = 0

    # Row uniqueness
    for row in grid:
        fitness += 9 - len(set(row))
    
    # Column uniqueness
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        fitness += 9 - len(set(column))
    
    # Block uniqueness
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

def crossover(parent1, parent2):
    """Perform crossover by combining rows from two parents."""
    crossover_point = random.randint(1, 8)
    return parent1[:crossover_point] + parent2[crossover_point:]

def mutate(individual, fixed_cells):
    """Mutate an individual by swapping non-fixed cells in a row."""
    for _ in range(2):  # Apply a few random swaps to increase diversity
        row = random.randint(0, 8)
        mutable_indices = [col for col in range(9) if not fixed_cells[row][col]]
        if len(mutable_indices) > 1:
            i, j = random.sample(mutable_indices, 2)
            individual[row][i], individual[row][j] = individual[row][j], individual[row][i]

def genetic_algorithm(grid, generations, population_size, mutation_rate):
    """Solve Sudoku using a genetic algorithm."""
    fixed_cells = get_fixed_cells(grid)
    population = create_population(grid, population_size)

    for generation in range(generations):
        # Evaluate fitness
        population.sort(key=fitness_function)
        best_fitness = fitness_function(population[0])

        # Check if the best solution is valid
        if best_fitness == 0:
            return population[0], generation

        # Select top individuals for breeding
        selected = population[: population_size // 2]

        # Generate next generation through crossover and mutation
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            offspring = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                mutate(offspring, fixed_cells)
            new_population.append(offspring)

        population = new_population

    # Return the best solution found
    return population[0], generations

def print_grid(grid):
    """Print a Sudoku grid."""
    for row in grid:
        print(row)

def main():
    print("Initial Puzzle:")
    print_grid(puzzle)

    solution, generations = genetic_algorithm(puzzle, GENERATIONS, POPULATION_SIZE, MUTATION_RATE)

    if is_valid_solution(solution):
        print("\nSolved Sudoku in {} generations:".format(generations))
        print_grid(solution)
    else:
        print("\nBest Attempt after {} generations:".format(generations))
        print_grid(solution)

if __name__ == "__main__":
    main()
