import random
import numpy as np

def initialize_grid(size=9):
    """Creates an empty Sudoku grid as a NumPy array."""
    return np.zeros((size, size), dtype=int)

def get_box_index(row, col, SRN):
    """Calculates the index of the sub-grid (box) for a given cell."""
    return (row // SRN) * SRN + (col // SRN)

def is_valid(grid, row, col, num, row_sets, col_sets, box_sets, SRN):
    """Checks if a number can be placed in a given cell."""
    box_idx = get_box_index(row, col, SRN)
    return (num not in row_sets[row] and 
            num not in col_sets[col] and 
            num not in box_sets[box_idx])

def add_number(grid, row, col, num, row_sets, col_sets, box_sets, SRN):
    """Adds a number to the grid and updates tracking sets."""
    box_idx = get_box_index(row, col, SRN)
    grid[row, col] = num
    row_sets[row].add(num)
    col_sets[col].add(num)
    box_sets[box_idx].add(num)

def remove_number(grid, row, col, num, row_sets, col_sets, box_sets, SRN):
    """Removes a number from the grid and updates tracking sets."""
    box_idx = get_box_index(row, col, SRN)
    grid[row, col] = 0
    row_sets[row].remove(num)
    col_sets[col].remove(num)
    box_sets[box_idx].remove(num)

def fill_box(grid, start_row, start_col, SRN, row_sets, col_sets, box_sets):
    """Fills a 3x3 sub-grid with random numbers."""
    numbers = list(range(1, SRN * SRN + 1))
    random.shuffle(numbers)
    for i in range(SRN):
        for j in range(SRN):
            row, col = start_row + i, start_col + j
            add_number(grid, row, col, numbers[i * SRN + j], row_sets, col_sets, box_sets, SRN)

def fill_remaining(grid, row, col, N, SRN, row_sets, col_sets, box_sets):
    """Uses backtracking to fill the rest of the grid."""
    if col >= N:
        row += 1
        col = 0
    if row >= N:
        return True
    if grid[row, col] != 0:
        return fill_remaining(grid, row, col + 1, N, SRN, row_sets, col_sets, box_sets)
    
    for num in random.sample(range(1, N + 1), N):
        if is_valid(grid, row, col, num, row_sets, col_sets, box_sets, SRN):
            add_number(grid, row, col, num, row_sets, col_sets, box_sets, SRN)
            if fill_remaining(grid, row, col + 1, N, SRN, row_sets, col_sets, box_sets):
                return True
            remove_number(grid, row, col, num, row_sets, col_sets, box_sets, SRN)
    return False

def create_full_sudoku():
    """Generates a fully filled Sudoku grid as a NumPy array."""
    N = 9
    SRN = 3
    grid = initialize_grid(N)
    row_sets = [set() for _ in range(N)]
    col_sets = [set() for _ in range(N)]
    box_sets = [set() for _ in range(N)]
    
    # Fill diagonal boxes
    for i in range(0, N, SRN):
        fill_box(grid, i, i, SRN, row_sets, col_sets, box_sets)
    
    # Fill the rest of the grid
    fill_remaining(grid, 0, SRN, N, SRN, row_sets, col_sets, box_sets)
    return grid

def create_puzzle(grid, difficulty="medium"):
    """Removes numbers from a full Sudoku grid to create a puzzle."""
    difficulty_map = {"easy": 30, "medium": 40, "hard": 50}
    cells_to_remove = difficulty_map.get(difficulty, 40)
    
    N = len(grid)
    cells = [(i, j) for i in range(N) for j in range(N)]
    random.shuffle(cells)
    
    for row, col in cells[:cells_to_remove]:
        grid[row, col] = 0

def generate_sudoku(difficulty="medium"):
    """Main function to generate a Sudoku puzzle with adjustable difficulty."""
    full_grid = create_full_sudoku()
    create_puzzle(full_grid, difficulty)
    return full_grid

# Example usage
if __name__ == "__main__":
    puzzle = generate_sudoku(difficulty="easy")
    print(puzzle)  # Only for testing purposes