const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8002';

// Hardened Payload Limits
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));
app.use(cors());

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB Successfully'))
  .catch(err => console.error('MongoDB connection error:', err));

// Storyboard Schema
const storyboardSchema = new mongoose.Schema({
  originalText: String,
  style: String,
  panels: Array,
  createdAt: { type: Date, default: Date.now }
});

const Storyboard = mongoose.model('Storyboard', storyboardSchema);

// Generation Bridge
app.post('/api/storyboard/generate', async (req, res) => {
  const { text, style } = req.body;
  
  if (!text) {
    return res.status(400).json({ success: false, error: 'Text input is required' });
  }

  console.log(`Forwarding request to AI Service: ${PYTHON_API_URL}/generate`);
  
  try {
    const aiResponse = await axios.post(`${PYTHON_API_URL}/generate`, {
      text,
      style
    }, { timeout: 120000 }); // 2-minute persistence for high-res images

    if (aiResponse.data.success) {
      const newStoryboard = new Storyboard({
        originalText: text,
        style,
        panels: aiResponse.data.panels
      });
      await newStoryboard.save();
      res.json({ success: true, storyboard: newStoryboard });
    } else {
      res.status(500).json({ success: false, error: 'AI generation failed' });
    }
  } catch (error) {
    console.error('Bridge Error:', error.message);
    res.status(500).json({ 
      success: false, 
      error: `AI Service Error: ${error.message}. Is the AI Service running on ${PYTHON_API_URL}?` 
    });
  }
});

// Database Get
app.get('/api/storyboard/:id', async (req, res) => {
  try {
    const storyboard = await Storyboard.findById(req.params.id);
    if (!storyboard) return res.status(404).json({ success: false, error: 'Not found' });
    res.json({ success: true, storyboard });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Node Backend running on http://localhost:${PORT}`);
});
