const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

router.post('/generate', (req, res) => {
  const { topic, difficulty, number } = req.body;
  
  // Spawn the Python script
  const pythonProcess = spawn('python3', [
    path.join(__dirname, '../../python_scripts/quizgen.py'),
    topic,
    difficulty,
    number
  ]);

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: 'Script execution failed' });
    }

    // Fetch generated quizzes from database
    const db = new sqlite3.Database('./databases/quiz.db');
    
    db.all('SELECT * FROM questions', (err, rows) => {
      db.close();
      if (err) {
        return res.status(500).json({ error: 'Database query failed' });
      }
      res.json(rows);
    });
  });
});

router.post('/check-proficiency', (req, res) => {
  const { 
    currentProficiency, 
    quizDifficulty, 
    quizScore, 
    numQuestions 
  } = req.body;
  
  // Spawn the Python script
  const pythonProcess = spawn('python3', [
    path.join(__dirname, '../../python_scripts/proficieny.py'),
    currentProficiency.toString(),
    quizDifficulty,
    quizScore.toString(),
    numQuestions.toString()
  ]);

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: 'Script execution failed' });
    }

    // For proficiency, you might want to add more sophisticated tracking
    res.json({ 
      currentProficiency, 
      newProficiency: currentProficiency + 5  // Simple increment for demonstration
    });
  });
});

module.exports = router;