import random

class SudokuOptimized9x9:
    def __init__(self):
        self.N = 9            # Grid size
        self.SRN = 3          # Square root of N
        self.grid = [[0] * self.N for _ in range(self.N)]
        self.row_sets = [set() for _ in range(self.N)]
        self.col_sets = [set() for _ in range(self.N)]
        self.box_sets = [set() for _ in range(self.N)]
        self.empty_cells = []
        
    def get_box_index(self, row, col):
        return (row // self.SRN) * self.SRN + (col // self.SRN)
    
    def is_valid_fast(self, row, col, num):
        box_idx = self.get_box_index(row, col)
        return (num not in self.row_sets[row] and 
                num not in self.col_sets[col] and 
                num not in self.box_sets[box_idx])
    
    def add_number(self, row, col, num):
        box_idx = self.get_box_index(row, col)
        self.grid[row][col] = num
        self.row_sets[row].add(num)
        self.col_sets[col].add(num)
        self.box_sets[box_idx].add(num)
    
    def remove_number(self, row, col, num):
        box_idx = self.get_box_index(row, col)
        self.grid[row][col] = 0
        self.row_sets[row].remove(num)
        self.col_sets[col].remove(num)
        self.box_sets[box_idx].remove(num)
    
    def get_possible_numbers(self, row, col):
        box_idx = self.get_box_index(row, col)
        all_numbers = set(range(1, self.N + 1))
        used_numbers = (self.row_sets[row] | 
                       self.col_sets[col] | 
                       self.box_sets[box_idx])
        return list(all_numbers - used_numbers)
    
    def fill_grid(self):
        # Fill diagonal boxes first
        for i in range(0, self.N, self.SRN):
            self.fill_box(i, i)
        
        # Fill remaining cells using backtracking
        return self.fill_remaining(0, self.SRN)
    
    def fill_box(self, start_row, start_col):
        numbers = list(range(1, self.N + 1))
        random.shuffle(numbers)
        for i in range(self.SRN):
            for j in range(self.SRN):
                row, col = start_row + i, start_col + j
                self.add_number(row, col, numbers[i * self.SRN + j])
    
    def fill_remaining(self, row, col):
        if col >= self.N:
            row += 1
            col = 0
        
        if row >= self.N:
            return True
        
        if self.grid[row][col] != 0:
            return self.fill_remaining(row, col + 1)
        
        possible_nums = self.get_possible_numbers(row, col)
        random.shuffle(possible_nums)
        
        for num in possible_nums:
            if self.is_valid_fast(row, col, num):
                self.add_number(row, col, num)
                if self.fill_remaining(row, col + 1):
                    return True
                self.remove_number(row, col, num)
        
        return False
    
    def create_puzzle(self):
        self.fill_grid()
        self.create_holes()
    
    def create_holes(self):
        cells = [(i, j) for i in range(self.N) for j in range(self.N)]
        cells_to_remove = 40  # Adjustable difficulty
        random.shuffle(cells)
        
        for row, col in cells[:cells_to_remove]:
            if self.grid[row][col] != 0:
                num = self.grid[row][col]
                self.remove_number(row, col, num)
                self.empty_cells.append((row, col))
    
    def print_grid(self):
        for i in range(self.N):
            if i % self.SRN == 0 and i != 0:
                print("-" * (self.N * 2 + self.SRN + 1))
            for j in range(self.N):
                if j % self.SRN == 0 and j != 0:
                    print("|", end=" ")
                if j == self.N - 1:
                    print(f"{self.grid[i][j]:2}", end="\n")
                else:
                    print(f"{self.grid[i][j]:2}", end=" ")

def generate_sudoku():
    sudoku = SudokuOptimized9x9()
    sudoku.create_puzzle()
    #print("\nGenerated 9x9 Sudoku Puzzle:")
    #print("=" * (9 * 2 + 4))
    sudoku.print_grid()
    #print("=" * (9 * 2 + 4))

# Generate a puzzle
if __name__ == "__main__":
    generate_sudoku()