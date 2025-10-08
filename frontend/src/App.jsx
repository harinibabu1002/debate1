import { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';  // <-- Env for Docker/local

function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/generate`, { prompt });
      setResponse(res.data.output);
    } catch (error) {
      setResponse(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>AI Tweet Generator</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter prompt (e.g., AI Agents taking over content creation)"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>Generate</button>
      </form>
      {loading && <p>Generating...</p>}
      {response && <pre>{response}</pre>}
    </div>
  );
}

export default App;