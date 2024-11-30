const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

router.post('/generate', (req, res) => {
  const { topic, duration } = req.body;
  
  // Spawn the Python script
  const pythonProcess = spawn('python3', [
    path.join(__dirname, '../../python_scripts/roadmap.py'),
    topic,
    duration
  ]);

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: 'Script execution failed' });
    }

    // Connect to SQLite and fetch the generated roadmap
    const db = new sqlite3.Database('./databases/study_plans.db');
    const tableName = topic.replace(/ /g, '_');
    
    db.all(`SELECT * FROM '${tableName}'`, (err, rows) => {
      db.close();
      if (err) {
        return res.status(500).json({ error: 'Database query failed' });
      }
      res.json(rows);
    });
  });
});

module.exports = router;