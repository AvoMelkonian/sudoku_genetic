'use client'
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

  const handleSolve = async () => {
    setLoading(true);
    setPuzzle(null);
    setSolvedPuzzle(null);
    setGenerationFound(null);

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
      setPuzzle(data.originalPuzzle);
      setSolvedPuzzle(data.solvedPuzzle);
      setGenerationFound(data.generationFound);
    } catch (error) {
      console.error("Error solving puzzle:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <div style={{ display: "flex", justifyContent: "center", marginBottom: "20px" }}>
        <Inputs config={config} setConfig={setConfig} onSolve={handleSolve} />
      </div>

      <div style={{ display: "flex", justifyContent: "space-evenly", alignItems: "center" }}>
        {puzzle && <SudokuGrid grid={puzzle} title="Generated Puzzle" />}
        {loading && <CircularProgress />}
        {solvedPuzzle && <SudokuGrid grid={solvedPuzzle} title="Solved Puzzle" />}
      </div>

      <div style={{ marginTop: "20px", textAlign: "left" }}>
        {generationFound !== null && (
          <p>
            <strong>Solution found in generation:</strong> {generationFound}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
