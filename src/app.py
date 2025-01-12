from flask import Flask, request, jsonify
import numpy as np
from ga_sudoku import genetic_algorithm, backtrack, fitness
from sudoku_generator import generate_sudoku
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        puzzle = np.array(data.get('puzzle')) if data.get('puzzle') else generate_sudoku(data.get('difficulty', 'easy'))

        # Solve the puzzle
        solved_puzzle, generation_found = genetic_algorithm(
            puzzle,
            generations=data.get('generations', 2000),
            population_size=data.get('populationSize', 170),
            mutation_rate=data.get('mutationRate', 0.25),
            elite_fraction=data.get('eliteFraction', 0.25),
            selection_type=data.get('selectionType', 'roulette')
        )

        # Calculate fitness
        fitness_value = fitness(solved_puzzle)
        is_valid = fitness_value == 243

        # Refine with backtracking or lightweight refinement
        if not is_valid:
            backtrack(solved_puzzle)
            fitness_value = fitness(solved_puzzle)
            is_valid = fitness_value == 243

        response = {
            "originalPuzzle": puzzle.tolist(),
            "solvedPuzzle": solved_puzzle.tolist() if is_valid else None,
            "bestCandidate": solved_puzzle.tolist() if not is_valid else None,
            "generationFound": generation_found,
            "fitness": fitness_value,
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
