'''from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/data')
def data():
    return jsonify({"message": "Hello from Flask API!"})

if __name__ == '__main__':
    app.run(debug=True)'''

from flask import Flask, request, jsonify
import numpy as np
from sudoku_generator import generate_sudoku
from ga_sudoku import genetic_algorithm, backtrack

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve():
    try:
        # Parse input data
        data = request.json
        difficulty = data.get('difficulty', 'easy')
        generations = data.get('generations', 2000)
        population_size = data.get('populationSize', 170)
        mutation_rate = data.get('mutationRate', 0.25)
        elite_fraction = data.get('eliteFraction', 0.25)
        selection_type = data.get('selectionType', 'roulette')

        # Generate or receive the puzzle
        puzzle = np.array(data.get('puzzle')) if data.get('puzzle') else generate_sudoku(difficulty)

        # Solve the puzzle
        solved_puzzle, generation_found = genetic_algorithm(
            puzzle,
            generations=generations,
            population_size=population_size,
            mutation_rate=mutation_rate,
            elite_fraction=elite_fraction,
            selection_type=selection_type
        )

        # Refine with backtracking if the solution isn't valid
        if not is_valid_solution(solved_puzzle):
            backtrack(solved_puzzle)

        # Prepare response
        response = {
            "originalPuzzle": puzzle.tolist(),
            "solvedPuzzle": solved_puzzle.tolist(),
            "generationFound": generation_found,
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def is_valid_solution(grid):
    """Validate the Sudoku grid."""
    for i in range(9):
        if len(set(grid[i])) != 9 or len(set(grid[:, i])) != 9:
            return False
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            subgrid = grid[row:row+3, col:col+3].flatten()
            if len(set(subgrid)) != 9:
                return False
    return True


if __name__ == '__main__':
    app.run(debug=True)

