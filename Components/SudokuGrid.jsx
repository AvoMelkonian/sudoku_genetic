// Components/SudokuGrid.js
import React from "react";

function SudokuGrid({ grid, title }) {
  if (!grid) {
    return <p>{title}: No grid to display</p>;
  }
  return (
    <div>
      <h3>{title}</h3>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(9, 40px)",
          gap: "2px",
        }}
      >
        {grid.flat().map((value, index) => (
          <div
            key={index}
            style={{
              width: "40px",
              height: "40px",
              textAlign: "center",
              lineHeight: "40px",
              border: "1px solid #ddd",
              backgroundColor: value === 0 ? "#f9f9f9" : "#e0e0e0",
            }}
          >
            {value || ""}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SudokuGrid;
