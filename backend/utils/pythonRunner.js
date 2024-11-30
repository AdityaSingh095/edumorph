const { PythonShell } = require('python-shell');
const path = require('path');

function runPythonScript(scriptName, args = []) {
  return new Promise((resolve, reject) => {
    const options = {
      mode: 'json',
      pythonPath: 'python3',
      pythonOptions: ['-u'],
      scriptPath: path.join(__dirname, '..', 'python_scripts'),
      args: args
    };

    PythonShell.run(scriptName, options, (err, results) => {
      if (err) reject(err);
      else resolve(results);
    });
  });
}

module.exports = { runPythonScript };