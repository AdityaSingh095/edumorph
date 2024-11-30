import sys
import sqlite3
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

def load_or_create_model():
    # Check if a saved model exists, otherwise create and train
    try:
        model = tf.keras.models.load_model('proficiency_model.h5')
    except:
        # Your existing model creation and training logic
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(6,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        
        # Load or create default dataset
        df = pd.DataFrame({
            'current_proficiency': [70, 60, 80],
            'quiz_difficulty': [1, 1, 1],
            'quiz_score': [80, 70, 90],
            'num_questions': [10, 10, 10],
            'new_proficiency': [75, 65, 85]
        })
        
        # Prepare features
        X = df[['current_proficiency', 'quiz_difficulty', 'quiz_score', 'num_questions']]
        y = df['new_proficiency']
        
        # Train the model
        model.fit(X, y, epochs=10, verbose=0)
        
        # Save the model
        model.save('proficiency_model.h5')
    
    return model

def predict_proficiency(model, current_proficiency, quiz_difficulty, quiz_score, num_questions):
    difficulty_mapping = {'easy': 0, 'medium': 1, 'hard': 2}
    difficulty_numeric = difficulty_mapping.get(quiz_difficulty, 1)
    
    input_data = np.array([[
        current_proficiency, 
        difficulty_numeric, 
        quiz_score, 
        num_questions,
        quiz_score / (num_questions * 5),
        current_proficiency - quiz_score
    ]])
    
    prediction = model.predict(input_data)[0][0]
    return np.clip(prediction, 0, 100)

def main():
    # Validate input
    if len(sys.argv) != 5:
        print("Usage: python proficieny.py current_proficiency difficulty quiz_score num_questions")
        sys.exit(1)
    
    current_proficiency = float(sys.argv[1])
    quiz_difficulty = sys.argv[2]
    quiz_score = float(sys.argv[3])
    num_questions = int(sys.argv[4])
    
    # Load or create model
    model = load_or_create_model()
    
    # Predict new proficiency
    new_proficiency = predict_proficiency(
        model, 
        current_proficiency, 
        quiz_difficulty, 
        quiz_score, 
        num_questions
    )
    
    # Store result in database
    conn = sqlite3.connect('proficiency.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proficiency_tracking (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            current_proficiency REAL,
            quiz_difficulty TEXT,
            quiz_score REAL,
            new_proficiency REAL
        )
    ''')
    
    # Insert tracking record
    cursor.execute('''
        INSERT INTO proficiency_tracking 
        (current_proficiency, quiz_difficulty, quiz_score, new_proficiency) 
        VALUES (?, ?, ?, ?)
    ''', (current_proficiency, quiz_difficulty, quiz_score, new_proficiency))
    
    conn.commit()
    conn.close()
    
    # Print result for parent process
    print(f"{new_proficiency}")

if __name__ == "__main__":
    main()