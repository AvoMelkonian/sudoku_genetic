'use client'
import React, { useEffect, useState } from 'react';

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
    </div>
  );
};

export default APIPage;
