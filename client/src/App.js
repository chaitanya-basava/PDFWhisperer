import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
    fetch(`${API_URL}/api/`)
      .then(response => response.json())
      .then(data => setMessage(data.message))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>{message}</p>
      </header>
    </div>
  );
}

export default App;
