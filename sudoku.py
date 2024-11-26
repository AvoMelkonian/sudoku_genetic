import random

POPULATION_SIZE = 100

puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

def create_individual(initial_grid):
    """
    Create a potential Sudoku solution based on the initial grid
    
    :param initial_grid: 9x9 list with pre-filled numbers
    :return: A copy of the grid with empty cells filled randomly
    """
    # Create a deep copy of the initial grid
    individual = [row[:] for row in initial_grid]
    
    # Fill in empty cells with random numbers
    for row in range(9):
        for col in range(9):
            if individual[row][col] == 0:
                individual[row][col] = random.randint(1, 9)
    
    return individual

def create_population(initial_grid, population_size):
    """
    Create a population of potential Sudoku solutions
    
    :param initial_grid: Initial Sudoku grid
    :param population_size: Number of individuals to generate
    :return: List of potential Sudoku solutions
    """
    return [create_individual(initial_grid) for _ in range(population_size)]

def main():
    # Create population
    population = create_population(puzzle, POPULATION_SIZE)
    
    # Print first few individuals
    print("Initial Population (first 3 individuals):")
    for i, individual in enumerate(population[:3], 1):
        print(f"\nIndividual {i}:")
        for row in individual:
            print(row)

# Run the main program
if __name__ == "__main__":
    main()