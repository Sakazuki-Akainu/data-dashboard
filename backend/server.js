const express = require('express');
const app = express();
const uploadRoute = require('./routes/upload');
require('./config/db');
require('dotenv').config();

app.use(express.json());
app.use('/upload', uploadRoute);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
