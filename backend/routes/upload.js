const express = require('express');
const router = express.Router();
const Upload = require('../models/Upload');
const multer = require('multer');
const axios = require('axios');
const upload = multer({ dest: '../assets/uploads/' });

router.post('/', upload.single('file'), async (req, res) => {
  try {
    const filePath = req.file.path;
    const response = await axios.post('http://localhost:8000/generate', { filePath });
    const graphs = response.data.graphs;

    const newUpload = new Upload({ file: req.file.originalname, graphs });
    await newUpload.save();

    res.json({ graphs });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
