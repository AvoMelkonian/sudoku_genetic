'use client';
import React, { useState } from "react";
import Inputs from "../Components/Inputs";
import SudokuGrid from "../Components/SudokuGrid";
import { CircularProgress, Box, Typography, Paper, Container } from "@mui/material";

function App() {
  const [config, setConfig] = useState({
    difficulty: "easy",
    generations: 1000,
    populationSize: 170,
    mutationRate: 0.25,
    eliteFraction: 0.25,
    selectionType: "roulette",
  });
  const [loading, setLoading] = useState(false);
  const [isSolved, setIsSolved] = useState(false); // Track if solving has been completed
  const [puzzle, setPuzzle] = useState(null);
  const [solvedPuzzle, setSolvedPuzzle] = useState(null);
  const [generationFound, setGenerationFound] = useState(null);
  const [isValidSolution, setIsValidSolution] = useState(false);

  const handleSolve = async () => {
    setLoading(true);
    setIsSolved(false); // Reset the solved state
    setPuzzle(null);
    setSolvedPuzzle(null);
    setGenerationFound(null);
    setIsValidSolution(false);

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
      setSolvedPuzzle(data.solvedPuzzle || data.bestCandidate); // Use best candidate if no solution
      setGenerationFound(data.generationFound);
      setIsValidSolution(data.isValidSolution);
      setIsSolved(true);
    } catch (error) {
      console.error("Error solving puzzle:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ padding: 4, textAlign: "center" }}>
      {/* Header */}
      <Typography variant="h4" gutterBottom>
        Sudoku Genetic Algorithm Solver
      </Typography>

      {/* Inputs Section */}
      <Paper
        elevation={3}
        sx={{
          padding: 3,
          marginBottom: 4,
          backgroundColor: "#f5f5f5",
          borderRadius: 4,
        }}
      >
        <Inputs config={config} setConfig={setConfig} onSolve={handleSolve} />
      </Paper>

      {/* Main Content Section */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-evenly",
          alignItems: "flex-start",
          flexWrap: "wrap",
          gap: 4,
        }}
      >
        {/* Generated Puzzle */}
        {puzzle && (
          <SudokuGrid grid={puzzle} title="Generated Puzzle" />
        )}

        {/* Solved Puzzle or Best Candidate */}
        {solvedPuzzle && (
          <SudokuGrid
            grid={solvedPuzzle}
            title={isValidSolution ? "Solved Puzzle" : "Best Candidate"}
          />
        )}

        {/* Loader */}
        {loading && (
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 1,
            }}
          >
            <CircularProgress />
            <Typography variant="body1">Solving...</Typography>
          </Box>
        )}
      </Box>

      {/* Results Section */}
      {isSolved && (
        <Box
          sx={{
            marginTop: 4,
            padding: 2,
            border: "1px solid #ccc",
            borderRadius: 2,
            backgroundColor: "#e3f2fd",
          }}
        >
          {generationFound !== null && (
            <Typography variant="body1">
              <strong>Solution found in generation:</strong> {generationFound}
            </Typography>
          )}
          <Typography
            variant="body1"
            sx={{ color: isValidSolution ? "green" : "red" }}
          >
            {isValidSolution
              ? "A valid solution was found."
              : "No valid solution was found. Displaying the best candidate."}
          </Typography>
        </Box>
      )}
    </Container>
  );
}

export default App;
