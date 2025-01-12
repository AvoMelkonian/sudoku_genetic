import React from "react";
import {
  Box,
  Button,
  Typography,
  Slider,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
} from "@mui/material";

function Inputs({ config, setConfig, onSolve }) {
  const handleInputChange = (key, value) => {
    setConfig({ ...config, [key]: value });
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 2,
        padding: 3,
        border: "1px solid #ccc",
        borderRadius: 4,
        backgroundColor: "#f9f9f9",
        boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
        width: "400px",
      }}
    >
      <Typography variant="h6" sx={{ marginBottom: 2 }}>
        Configure Genetic Algorithm
      </Typography>

      {/* Difficulty */}
      <FormControl fullWidth>
        <InputLabel sx={{marginTop: -1}}>Difficulty</InputLabel>
        <Select
          value={config.difficulty}
          onChange={(e) => handleInputChange("difficulty", e.target.value)}
        >
          <MenuItem value="easy">Easy</MenuItem>
          <MenuItem value="medium">Medium</MenuItem>
          <MenuItem value="hard">Hard</MenuItem>
        </Select>
      </FormControl>

      {/* Generations */}
      <Typography variant="body1" gutterBottom>
        Generations: {config.generations}
      </Typography>
      <Slider
        value={config.generations}
        min={1000}
        max={5000}
        step={100}
        onChange={(e, value) => handleInputChange("generations", value)}
      />

      {/* Population Size */}
      <Typography variant="body1" gutterBottom>
        Population Size: {config.populationSize}
      </Typography>
      <Slider
        value={config.populationSize}
        min={50}
        max={300}
        step={10}
        onChange={(e, value) => handleInputChange("populationSize", value)}
      />

      {/* Mutation Rate */}
      <Typography variant="body1" gutterBottom>
        Mutation Rate: {config.mutationRate.toFixed(2)}
      </Typography>
      <Slider
        value={config.mutationRate}
        min={0.1}
        max={0.5}
        step={0.05}
        onChange={(e, value) =>
          handleInputChange("mutationRate", parseFloat(value))
        }
      />

      {/* Elite Fraction */}
      <Typography variant="body1" gutterBottom>
        Elite Fraction: {config.eliteFraction.toFixed(2)}
      </Typography>
      <Slider
        value={config.eliteFraction}
        min={0.1}
        max={0.5}
        step={0.05}
        onChange={(e, value) =>
          handleInputChange("eliteFraction", parseFloat(value))
        }
      />

      {/* Selection Type */}
      <FormControl fullWidth>
        <InputLabel sx={{marginTop: -1}}>Selection Type</InputLabel>
        <Select
          value={config.selectionType}
          onChange={(e) => handleInputChange("selectionType", e.target.value)}
        >
          <MenuItem value="roulette">Roulette</MenuItem>
          <MenuItem value="tournament">Tournament</MenuItem>
        </Select>
      </FormControl>

      {/* Generate and Solve Button */}
      <Button
        variant="contained"
        color="primary"
        onClick={onSolve}
        sx={{
          marginTop: 2,
          textTransform: "none",
        }}
      >
        Generate and Solve
      </Button>
    </Box>
  );
}

export default Inputs;
