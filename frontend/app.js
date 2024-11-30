async function generateRoadmap() {
    const topic = document.getElementById('topic').value;
    const duration = document.getElementById('duration').value;
    const resultsDiv = document.getElementById('roadmap-results');

    try {
        const response = await fetch('/api/roadmap/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, duration })
        });
        const roadmap = await response.json();
        
        resultsDiv.innerHTML = roadmap.map(item => `
            <div class="roadmap-item">
                <h3>${item.subtopic}</h3>
                <p>Description: ${item.description}</p>
                <p>Study Material: ${item.study_material}</p>
                <p>Time: ${item.time_to_be_given}</p>
            </div>
        `).join('');
    } catch (error) {
        resultsDiv.innerHTML = `Error: ${error.message}`;
    }
}

async function generateQuiz() {
    const topic = document.getElementById('quiz-topic').value;
    const difficulty = document.getElementById('quiz-difficulty').value;
    const number = document.getElementById('quiz-number').value;
    const resultsDiv = document.getElementById('quiz-results');

    try {
        const response = await fetch('/api/quiz/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, difficulty, number })
        });
        const quizzes = await response.json();
        
        resultsDiv.innerHTML = quizzes.map(quiz => `
            <div class="quiz-item">
                <p>${quiz.question}</p>
                <div class="options">
                    <label><input type="radio" name="q${quiz.id}">A) ${quiz.option_a}</label>
                    <label><input type="radio" name="q${quiz.id}">B) ${quiz.option_b}</label>
                    <label><input type="radio" name="q${quiz.id}">C) ${quiz.option_c}</label>
                    <label><input type="radio" name="q${quiz.id}">D) ${quiz.option_d}</label>
                </div>
            </div>
        `).join('');
    } catch (error) {
        resultsDiv.innerHTML = `Error: ${error.message}`;
    }
}

async function updateProficiency() {
    const userId = 'user123'; // This would typically come from authentication
    const topic = document.getElementById('topic').value;
    const currentProficiency = 70; // This would come from user's current state
    const quizScore = calculateQuizScore(); // Method to calculate quiz score
    const quizDifficulty = document.getElementById('quiz-difficulty').value;

    try {
        const response = await fetch('/api/proficiency/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                userId, 
                topic, 
                currentProficiency, 
                quizScore, 
                quizDifficulty 
            })
        });
        const proficiencyUpdate = await response.json();
        
        // Display proficiency update
        document.getElementById('proficiency-result').innerHTML = `
            Proficiency updated from ${proficiencyUpdate.oldProficiency} 
            to ${proficiencyUpdate.newProficiency}
        `;
    } catch (error) {
        console.error('Proficiency update failed:', error);
    }
}