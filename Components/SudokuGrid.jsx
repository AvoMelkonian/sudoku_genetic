import React from "react";
import { Box, Typography } from "@mui/material";

function SudokuGrid({ grid, title }) {
  if (!grid) {
    return <Typography variant="body1">{title}: No grid to display</Typography>;
  }

  return (
    <Box sx={{ textAlign: "center", marginBottom: 4 }}>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "repeat(9, 40px)",
          gap: "4px",
          justifyContent: "center",
        }}
      >
        {grid.flat().map((value, index) => (
          <Box
            key={index}
            sx={{
              width: "40px",
              height: "40px",
              textAlign: "center",
              lineHeight: "40px",
              border: "1px solid #ddd",
              backgroundColor: value === 0 ? "#f5f5f5" : "#e0e0e0",
              fontFamily: "monospace",
              fontWeight: value === 0 ? "normal" : "bold",
              fontSize: "16px",
              color: value === 0 ? "#aaa" : "#000",
              borderRadius: "4px", // Rounded corners
            }}
          >
            {value || ""}
          </Box>
        ))}
      </Box>
    </Box>
  );
}

export default SudokuGrid;
