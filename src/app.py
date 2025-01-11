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
from ga_sudoku import genetic_algorithm, backtrack, is_valid_solution
from sudoku_generator import generate_sudoku  # Assume this module generates puzzles
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

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

        # Generate or use provided puzzle
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

        # Validate solution and refine with backtracking if necessary
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


if __name__ == '__main__':
    app.run(debug=True)
