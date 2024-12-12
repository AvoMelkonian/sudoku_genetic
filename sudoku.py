from itertools import chain
import random

def validate_rows(grid):
    """
    Validates that each row in the grid contains unique numbers (ignoring 0).
    """
    def is_valid_row(row):
        numbers = [num for num in row if num != 0]
        return len(numbers) == len(set(numbers))

    return all(is_valid_row(row) for row in grid)

def validate_columns(grid):
    """
    Transpose the grid to convert columns into rows and
    validates that each column in the grid contains unique numbers (ignoring 0).
    """
    transposed = [list(col) for col in zip(*grid)]
    return validate_rows(transposed)

def validate_subgrids(grid):
    """
    Extract all 3x3 subgrids from the grid and
    validates that each 3x3 subgrid contains unique numbers (ignoring 0).
    """
    subgrids = []
    for row_block in range(0, 9, 3):
        for col_block in range(0, 9, 3):
            subgrid = list(
                chain(*[grid[row][col_block:col_block+3] for row in range(row_block, row_block+3)])
            )
            subgrids.append(subgrid)
    return validate_rows(subgrids)

def is_valid_sudoku(grid):
    """
    Validates the entire Sudoku grid by checking rows, columns, and subgrids.
    """
    return validate_rows(grid) and validate_columns(grid) and validate_subgrids(grid)

def initialize_population(grid, population_size=100):
    """
    Initializes a population of Sudoku grids by filling empty cells randomly.
    """
    def fill_grid(base_grid):
        new_grid = []
        for row in base_grid:
            new_row = [num if num != 0 else random.randint(1, 9) for num in row]
            new_grid.append(new_row)
        return new_grid
    return [fill_grid(grid) for _ in range(population_size)]

# Example Grid
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

#print("if sudoku is valid, then it is solvable",is_valid_sudoku(new_grid))

# Test Population Initialization
population = initialize_population(grid, population_size=5)
for i, individual in enumerate(population, 1):
    print(f"Individual {i}:")
    for row in individual:
        print(row)
    print()
