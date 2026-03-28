import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [pitch, setPitch] = useState('');
  const [style, setStyle] = useState('photorealistic');
  const [loading, setLoading] = useState(false);
  const [storyboard, setStoryboard] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.regen = false; // dummy
    e.preventDefault();
    if (!pitch.trim()) return;

    setLoading(true);
    setError(null);
    setStoryboard(null);

    try {
      const response = await axios.post('http://localhost:5001/api/stories/generate', {
        text: pitch,
        style: style
      });
      setStoryboard(response.data);
    } catch (err) {
      console.error(err);
      setError('Failed to generate storyboard. Check server logs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>The Pitch Visualizer</h1>
        <p>Transform your narrative into a compelling visual storyboard</p>
      </header>

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="pitch">Your Story / Pitch</label>
            <textarea 
              id="pitch"
              rows={6}
              placeholder="Enter your customer success story or product pitch here (e.g., The customer was overwhelmed with data. They implemented our solution. Their productivity skyrocketed.)"
              value={pitch}
              onChange={(e) => setPitch(e.target.value)}
              required
            ></textarea>
          </div>

          <div className="input-group">
            <label htmlFor="style">Visual Style</label>
            <select 
              id="style" 
              value={style} 
              onChange={(e) => setStyle(e.target.value)}
            >
              <option value="photorealistic">Photorealistic</option>
              <option value="cinematic">Cinematic Concept Art</option>
              <option value="comic-book">Comic Book Style</option>
              <option value="watercolor">Watercolor</option>
              <option value="3d-render">3D Render (Pixar style)</option>
              <option value="cyberpunk">Cyberpunk</option>
            </select>
          </div>

          <button type="submit" disabled={loading || !pitch.trim()}>
            {loading ? (
              <>
                <div className="spinner"></div> Processing AI Narrative...
              </>
            ) : "Generate Storyboard"}
          </button>
        </form>
        {error && <p style={{color: '#ff6b6b', marginTop: '1rem', textAlign: 'center'}}>{error}</p>}
      </div>

      {storyboard && storyboard.panels && (
        <div className="storyboard-container">
          <h2 style={{textAlign: 'center', marginBottom: '2rem', fontSize: '2rem'}}>Your Storyboard generated in '{storyboard.style}'</h2>
          {storyboard.panels.map((panel, idx) => (
            <div className="scene-card" key={idx} style={{animationDelay: `${idx * 0.2}s`}}>
              {panel.imageBase64 ? (
                <img 
                  src={`data:image/jpeg;base64,${panel.imageBase64}`} 
                  alt={`Scene ${idx + 1}`} 
                  className="scene-image" 
                />
              ) : (
                <div className="scene-image" style={{display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#222'}}>
                  Image failed to generate
                </div>
              )}
              <div className="scene-content">
                <div className="scene-number">Scene {idx + 1}</div>
                <div className="scene-text">"{panel.original_text}"</div>
                <div className="scene-prompt">
                  <strong>AI Prompt:</strong> {panel.engineered_prompt}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
