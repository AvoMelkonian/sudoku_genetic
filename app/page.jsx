'use client'
// App.js
import React, { useState } from "react";
import Inputs from "../Components/Inputs";
import SudokuGrid from "../Components/SudokuGrid";
import { CircularProgress } from "@mui/material";
import FitnessChart from "../Components/FitnessChart";

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
  const [fitnessData, setFitnessData] = useState([]);

  const handleSolve = async () => {
    setLoading(true);
    setPuzzle(null);
    setSolvedPuzzle(null);
  
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
      alert(`Solution found in generation: ${data.generationFound}`);
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
          alignItems: "center",
        }}
      >
        {/* Generated Puzzle */}
        {puzzle && (
          <SudokuGrid grid={puzzle} title="Generated Puzzle" />
        )}

        {/* Loader */}
        {loading && (
          <div>
            <CircularProgress />
            <p>Solving...</p>
          </div>
        )}

        {/* Solved Puzzle */}
        {solvedPuzzle && (
          <SudokuGrid grid={solvedPuzzle} title="Solved Puzzle" />
        )}
        <FitnessChart fitnessData={fitnessData} />
      </div>
    </div>
  );
}

// Mock Functions (Replace with API Calls)
const generatePuzzle = async (difficulty) => {
  await delay(1000); // Simulate delay
  return Array(9)
    .fill(0)
    .map(() => Array(9).fill(0)); // Replace with logic
};

const solvePuzzleWithFitnessUpdates = async (puzzle, config, updateFitness) => {
  const fitness = [];
  for (let gen = 0; gen < config.generations; gen++) {
    const randomFitness = Math.random() * 100; // Mock fitness values
    fitness.push(randomFitness);

    // Update the chart with the new fitness data
    updateFitness([...fitness]);

    // Check for a stopping condition (e.g., fitness > 95)
    if (randomFitness > 95) {
      console.log(`Stopping early at generation ${gen + 1} with fitness ${randomFitness}`);
      break;
    }

    await delay(100); // Simulate generation delay
  }
  return puzzle.map((row) =>
    row.map(() => Math.floor(Math.random() * 9) + 1)
  ); // Replace with logic
};


const solvePuzzle = async (puzzle, config) => {
  await delay(2000); // Simulate delay
  return puzzle.map((row) =>
    row.map(() => Math.floor(Math.random() * 9) + 1)
  ); // Replace with logic
};

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export default App;


/*import React, { useEffect, useState } from 'react';

const APIPage = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/data') // Ensure this URL is correct
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => setData(data))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);
  

  return (
    <div>
      <h1>Data from Flask</h1>
      {data ? <p>{data.message}</p> : <p>Loading...</p>}
      <SudokuSolverUI></SudokuSolverUI>
      <SudokuGrid></SudokuGrid>
    </div>
  );
};

export default APIPage;*/
