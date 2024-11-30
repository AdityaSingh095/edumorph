const express = require('express');
const cors = require('cors');
const roadmapRoutes = require('./routes/roadmap');
const quizRoutes = require('./routes/quiz');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Static frontend serving
app.use(express.static('../frontend'));

// Routes
app.use('/api/roadmap', roadmapRoutes);
app.use('/api/quiz', quizRoutes);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

const proficiencyRoutes = require('./routes/proficiency');
app.use('/api/proficiency', proficiencyRoutes);
