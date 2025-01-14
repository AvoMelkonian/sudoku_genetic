import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from flask import Flask, request, jsonify
import numpy as np
from ga_sudoku import genetic_algorithm, backtrack, fitness
from sudoku_generator import generate_sudoku
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://sudoku-genetic.vercel.app"]}})

@app.route('/solve', methods=['GET'])
def solve():
    try:
        data = request.json
        puzzle = np.array(data.get('puzzle')) if data.get('puzzle') else generate_sudoku(data.get('difficulty', 'easy'))

        # Solve the puzzle using the genetic algorithm
        solved_puzzle, generation_found = genetic_algorithm(
            puzzle,
            generations=data.get('generations', 2000),
            population_size=data.get('populationSize', 170),
            mutation_rate=data.get('mutationRate', 0.25),
            elite_fraction=data.get('eliteFraction', 0.25),
            selection_type=data.get('selectionType', 'roulette')
        )

        # Calculate fitness of the result
        fitness_value = fitness(solved_puzzle)
        is_valid_solution = fitness_value == 243

        # Refine with backtracking if needed
        if not is_valid_solution:
            backtrack(solved_puzzle)
            fitness_value = fitness(solved_puzzle)
            is_valid_solution = fitness_value == 243

        # Prepare the response
        response = {
            "originalPuzzle": puzzle.tolist(),
            "solvedPuzzle": solved_puzzle.tolist() if is_valid_solution else None,
            "bestCandidate": solved_puzzle.tolist() if not is_valid_solution else None,
            "generationFound": generation_found,
            "isValidSolution": is_valid_solution
        }
        return jsonify(response), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True)
