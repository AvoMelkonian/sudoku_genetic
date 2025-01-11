'use client'
// App.js
import React, { useState } from "react";
import Inputs from "../Components/Inputs";
import SudokuGrid from "../Components/SudokuGrid";
import { CircularProgress } from "@mui/material";

function App() {
  const [config, setConfig] = useState({
    difficulty: "easy",
    generations: 2000,
    populationSize: 170,
    mutationRate: 0.25,
    eliteFraction: 0.25,
    selectionType: "roulette",
  });
  const [loading, setLoading] = useState(false);
  const [puzzle, setPuzzle] = useState(null);
  const [solvedPuzzle, setSolvedPuzzle] = useState(null);
  const [generationFound, setGenerationFound] = useState(null);
  const [bestCandidate, setBestCandidate] = useState(null);

  const handleSolve = async () => {
    setLoading(true);
    setPuzzle(null);
    setSolvedPuzzle(null);
    setGenerationFound(null);
    setBestCandidate(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          difficulty: config.difficulty,
          generations: config.generations,
          populationSize: config.populationSize,
          mutationRate: config.mutationRate,
          eliteFraction: config.eliteFraction,
          selectionType: config.selectionType,
        }),
      });

      const data = await response.json();
      setPuzzle(data.originalPuzzle); // The original puzzle received from the server
      setSolvedPuzzle(data.solvedPuzzle); // The solved puzzle received from the server
      setGenerationFound(data.generationFound); // Display generation where solution was found
      setBestCandidate(data.bestCandidate); // Display best candidate if no solution
    } catch (error) {
      console.error("Error solving puzzle:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      {/* Controls */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "20px",
          marginBottom: "20px",
        }}
      >
        <Inputs config={config} setConfig={setConfig} onSolve={handleSolve} />
      </div>

      {/* Main Section */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-evenly",
          alignItems: "flex-start",
          gap: "40px",
        }}
      >
        {/* Generated Puzzle */}
        {puzzle && <SudokuGrid grid={puzzle} title="Generated Puzzle" />}

        {/* Loader */}
        {loading && (
          <div>
            <CircularProgress />
            <p>Solving...</p>
          </div>
        )}

        {/* Solved Puzzle */}
        {solvedPuzzle && <SudokuGrid grid={solvedPuzzle} title="Solved Puzzle" />}
      </div>

      {/* Results Section */}
      <div style={{ marginTop: "20px", textAlign: "left" }}>
      {generationFound !== null ? (
        <p>
          <strong>Solution found in generation:</strong> {generationFound}
        </p>
      ) : (
        bestCandidate && (
          <div>
            <p>
              <strong>No solution found. Best candidate:</strong>
            </p>
            <pre style={{ background: "#f4f4f4", padding: "10px", borderRadius: "5px" }}>
              {JSON.stringify(bestCandidate, null, 2)}
            </pre>
          </div>
        )
      )}
    </div>
    </div>
  );
}

export default App;
