const mongoose = require('mongoose');

const uploadSchema = new mongoose.Schema({
  file: String,
  graphs: Array,
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Upload', uploadSchema);
