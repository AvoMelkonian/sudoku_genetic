// Components/Inputs.js
import React from "react";

function Inputs({ config, setConfig, onSolve }) {
  const handleInputChange = (key, value) => {
    setConfig({ ...config, [key]: value });
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <h3>Configure Genetic Algorithm</h3>
      <label>Difficulty: </label>
      <select
        value={config.difficulty}
        onChange={(e) => handleInputChange("difficulty", e.target.value)}
      >
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
      </select>
      <div>
        <label>Generations: {config.generations}</label>
        <input
          type="range"
          min="1000"
          max="5000"
          step="100"
          value={config.generations}
          onChange={(e) => handleInputChange("generations", +e.target.value)}
        />
      </div>
      <div>
        <label>Population Size: {config.populationSize}</label>
        <input
          type="range"
          min="50"
          max="300"
          step="10"
          value={config.populationSize}
          onChange={(e) =>
            handleInputChange("populationSize", +e.target.value)
          }
        />
      </div>
      <div>
        <label>Mutation Rate: {config.mutationRate}</label>
        <input
          type="range"
          min="0.1"
          max="0.5"
          step="0.05"
          value={config.mutationRate}
          onChange={(e) =>
            handleInputChange("mutationRate", parseFloat(e.target.value))
          }
        />
      </div>
      <div>
        <label>Elite Fraction: {config.eliteFraction}</label>
        <input
          type="range"
          min="0.1"
          max="0.5"
          step="0.05"
          value={config.eliteFraction}
          onChange={(e) =>
            handleInputChange("eliteFraction", parseFloat(e.target.value))
          }
        />
      </div>
      <div>
        <label>Selection Type: </label>
        <select
          value={config.selectionType}
          onChange={(e) => handleInputChange("selectionType", e.target.value)}
        >
          <option value="roulette">Roulette</option>
          <option value="tournament">Tournament</option>
        </select>
      </div>
      <button onClick={onSolve}>Generate and Solve</button>
    </div>
  );
}

export default Inputs;
