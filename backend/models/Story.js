const mongoose = require('mongoose');

const panelSchema = new mongoose.Schema({
  original_text: { type: String, required: true },
  engineered_prompt: { type: String, required: true },
  imageBase64: { type: String }
});

const storySchema = new mongoose.Schema({
  original_pitch: { type: String, required: true },
  style: { type: String, default: "photorealistic" },
  panels: [panelSchema],
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Story', storySchema);
