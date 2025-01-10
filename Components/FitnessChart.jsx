// Components/FitnessChart.js
import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register the required Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function FitnessChart({ fitnessData }) {
  const data = {
    labels: fitnessData.map((_, index) => `Gen ${index + 1}`),
    datasets: [
      {
        label: "Fitness Score",
        data: fitnessData,
        fill: false,
        borderColor: "#4caf50",
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: "top",
      },
    },
    scales: {
      x: {
        type: "category", // Specify category scale for the x-axis
      },
      y: {
        type: "linear", // Specify linear scale for the y-axis
      },
    },
  };

  return (
    <div>
      <h3>Fitness Chart</h3>
      <Line data={data} options={options} />
    </div>
  );
}

export default FitnessChart;
