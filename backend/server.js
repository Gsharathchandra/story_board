require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const axios = require('axios');
const Story = require('./models/Story');

const app = express();
const PORT = process.env.PORT || 5001;
const PYTHON_API_URL = process.env.PYTHON_API_URL || "http://localhost:8000";

// Increase payload limit for base64 images
app.use(express.json({ limit: '50mb' }));
app.use(cors());

mongoose.connect(process.env.MONGODB_URI)
.then(() => console.log('Connected to MongoDB'))
.catch(err => console.error('MongoDB connection error:', err));

// Generate storyboard route
app.post('/api/stories/generate', async (req, res) => {
  try {
    const { text, style } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: "Text is required" });
    }

    // Call Python FastAPI service for AI processing
    const pythonRes = await axios.post(`${PYTHON_API_URL}/generate`, { text, style }, { timeout: 300000 }); // 5 minutes timeout
    const panels = pythonRes.data.panels;

    // Save history to MongoDB
    const newStory = new Story({
      original_pitch: text,
      style: style,
      panels: panels
    });

    const savedStory = await newStory.save();
    
    // Return to frontend
    res.status(200).json(savedStory);

  } catch (error) {
    console.error("Generate error:", error.response?.data || error.message);
    res.status(500).json({ error: "Failed to generate storyboard. Please try again later." });
  }
});

// Fetch all stories
app.get('/api/stories', async (req, res) => {
  try {
    const stories = await Story.find().sort({ createdAt: -1 });
    res.status(200).json(stories);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch stories" });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
