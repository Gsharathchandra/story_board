import React, { useState } from 'react';
import axios from 'axios';
import { Sparkles, Send, Image as ImageIcon, Loader2 } from 'lucide-react';

const API_URL = 'http://localhost:5001/api/storyboard/generate';

function App() {
  const [text, setText] = useState('');
  const [style, setStyle] = useState('photorealistic');
  const [loading, setLoading] = useState(false);
  const [storyboard, setStoryboard] = useState(null);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError('');
    setStoryboard(null);

    try {
      const res = await axios.post(API_URL, { text, style });
      if (res.data.success) {
        setStoryboard(res.data.storyboard);
      } else {
        setError('The AI is currently busy. Please try again in 10 seconds.');
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || 'Failed to connect to AI server. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f111a] text-white p-6 md:p-12 font-sans">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="mb-12 text-center animate-fade-in">
          <div className="inline-block p-3 bg-indigo-600/20 rounded-2xl mb-4">
            <Sparkles className="w-8 h-8 text-indigo-400" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            The Pitch Visualizer
          </h1>
          <p className="text-gray-400 text-lg">Rebuilt for Speed & High-Fidelity AI Generation</p>
        </header>

        {/* Input Section */}
        <div className="bg-[#1a1c2e] border border-white/5 rounded-3xl p-8 mb-12 shadow-2xl">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Your Story / Pitch</label>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="An apple tree standing in a sunlit field with ripe fruit..."
                className="w-full h-40 bg-[#0f111a] border border-white/5 rounded-2xl p-5 text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all resize-none"
              />
            </div>

            <div className="flex flex-col md:flex-row gap-6">
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-400 mb-2">Visual Style</label>
                <select
                  value={style}
                  onChange={(e) => setStyle(e.target.value)}
                  className="w-full bg-[#0f111a] border border-white/5 rounded-2xl p-4 focus:ring-2 focus:ring-indigo-500 outline-none appearance-none cursor-pointer"
                >
                  <option value="photorealistic">Cinematic Photorealistic</option>
                  <option value="comic-book">Vibrant Comic Book</option>
                  <option value="3d-render">Unreal Engine 5 Render</option>
                  <option value="oil-painting">Classic Oil Painting</option>
                </select>
              </div>
              <button
                onClick={handleGenerate}
                disabled={loading || !text.trim()}
                className="md:w-64 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-4 px-8 rounded-2xl flex items-center justify-center gap-3 transition-all active:scale-95 shadow-lg shadow-indigo-600/20"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    <span>Generate Storyboard</span>
                  </>
                )}
              </button>
            </div>

            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-400 flex items-center gap-3 animate-shake">
                <div className="w-2 h-2 rounded-full bg-red-400" />
                <span>{error}</span>
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        {storyboard && (
          <div className="space-y-12 animate-fade-in-up">
            <h2 className="text-2xl font-bold flex items-center gap-3 mb-8">
              <ImageIcon className="w-6 h-6 text-indigo-400" />
              Generated Storyboard
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {storyboard.panels.map((panel, idx) => (
                <div key={idx} className="group bg-[#1a1c2e] border border-white/5 rounded-3xl overflow-hidden hover:border-indigo-500/50 transition-all duration-500 hover:shadow-2xl hover:shadow-indigo-500/10">
                  <div className="aspect-[4/3] bg-[#0f111a] relative overflow-hidden">
                    {panel.imageBase64 ? (
                      <img
                        src={`data:image/png;base64,${panel.imageBase64}`}
                        alt={panel.original_text}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                      />
                    ) : (
                      <div className="w-full h-full flex flex-col items-center justify-center text-gray-600 gap-4">
                        <ImageIcon className="w-12 h-12 opacity-20" />
                        <span className="text-sm font-medium">Image processing...</span>
                      </div>
                    )}
                    <div className="absolute top-4 left-4 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full text-xs font-bold border border-white/10 uppercase tracking-wider text-indigo-300">
                      Scene {idx + 1}
                    </div>
                  </div>
                  <div className="p-6">
                    <p className="text-gray-300 leading-relaxed text-sm line-clamp-3">
                      "{panel.original_text}"
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
