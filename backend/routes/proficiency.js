const express = require('express');
const router = express.Router();
const { runPythonScript } = require('../utils/pythonRunner');

router.post('/predict', async (req, res) => {
  try {
    const { 
      currentProficiency, 
      quizDifficulty, 
      quizScore, 
      numQuestions 
    } = req.body;

    // Validate input
    if (!currentProficiency || !quizDifficulty || !quizScore || !numQuestions) {
      return res.status(400).json({ error: 'Missing required parameters' });
    }

    // Run proficiency prediction Python script
    const results = await runPythonScript('proficieny.py', [
      currentProficiency,
      quizDifficulty,
      quizScore,
      numQuestions
    ]);

    // The Python script should return the new predicted proficiency
    res.json({
      currentProficiency,
      newProficiency: results[0],
      improvement: results[0] - currentProficiency
    });

  } catch (error) {
    console.error('Proficiency prediction error:', error);
    res.status(500).json({ 
      error: 'Failed to predict proficiency', 
      details: error.message 
    });
  }
});

// Endpoint to track and update user proficiency
router.post('/update', async (req, res) => {
  try {
    const { 
      userId, 
      topic, 
      currentProficiency, 
      quizScore, 
      quizDifficulty 
    } = req.body;

    // You might want to add database logic here to persist proficiency updates
    const newProficiencyResult = await runPythonScript('proficieny.py', [
      currentProficiency,
      quizDifficulty,
      quizScore,
      // Assuming number of questions can be derived from quiz
      quizScore / 5  // Simple heuristic
    ]);

    res.json({
      userId,
      topic,
      oldProficiency: currentProficiency,
      newProficiency: newProficiencyResult[0]
    });

  } catch (error) {
    console.error('Proficiency update error:', error);
    res.status(500).json({ 
      error: 'Failed to update proficiency', 
      details: error.message 
    });
  }
});

// Endpoint to get user's proficiency history
router.get('/history/:userId/:topic', async (req, res) => {
  try {
    const { userId, topic } = req.params;

    // This would typically involve querying a database
    // For now, we'll return a mock response
    res.json({
      userId,
      topic,
      proficiencyHistory: [
        { date: '2024-01-01', proficiency: 50 },
        { date: '2024-02-01', proficiency: 65 },
        { date: '2024-03-01', proficiency: 75 }
      ]
    });

  } catch (error) {
    console.error('Proficiency history error:', error);
    res.status(500).json({ 
      error: 'Failed to retrieve proficiency history', 
      details: error.message 
    });
  }
});

module.exports = router;