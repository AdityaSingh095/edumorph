import google.generativeai as genai
import sqlite3
import re
import sys
import json

# Set your API key for Google Generative AI
API_KEY = "Your API key"  # Replace with your actual API key
genai.configure(api_key=API_KEY)


# Connect to the SQLite database
conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

# Drop the existing questions table if it exists
#cursor.execute("DROP TABLE IF EXISTS questions")

# Create the questions table with the correct structure
cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct_answer TEXT,
        difficulty TEXT,
        status TEXT DEFAULT invalid
    );
""")

def verify_table_structure():
    cursor.execute("PRAGMA table_info(questions)")
    columns = [col[1] for col in cursor.fetchall()]
    expected_columns = ['id', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer' ,'difficulty','status']
    if set(columns) != set(expected_columns):
        raise Exception(f"Table structure is incorrect. Expected columns: {expected_columns}, Got: {columns}")

def generate_quiz(prompt, difficulty):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    quiz_content = response.text
    print("Raw quiz content:")
    print(quiz_content)
    print("\n---\n")

    # Split the content into individual questions
    questions = re.split(r'\*\*\d+\.', quiz_content)[1:]  # Split by bold numbered questions

    for q in questions:
        # Extract question text
        question_match = re.match(r'\s*(.+?)\*\*\s*A\)', q, re.DOTALL)
        if not question_match:
            continue
        question_text = question_match.group(1).strip()

        # Extract options
        options = re.findall(r'([A-D]\)\s*.+?)(?=[A-D]\)|Correct Answer|\Z)', q, re.DOTALL)
        options = [opt.strip() for opt in options]

        # Extract correct answer
        correct_answer_match = re.search(r'Correct Answer:\s*\*\*([A-D])\*\*', q)
        correct_answer = correct_answer_match.group(1) if correct_answer_match else None

        if len(options) == 4 and correct_answer:
            try:
                cursor.execute("""
                    INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer, difficulty)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                """, (question_text, options[0], options[1], options[2], options[3], correct_answer, difficulty))
                print(f"Inserted question: {question_text[:30]}... with answer: {correct_answer}")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        else:
            print(f"Skipping question due to parsing issues: {question_text[:30]}...")

    conn.commit()
    return "Quiz generated and stored in database!"

def get_all_questions():
    cursor.execute("SELECT * FROM questions;")
    return cursor.fetchall()

# Verify table structure before proceeding
verify_table_structure()

# Generate a quiz
quiz_prompt = f"""Generate a JEE mains specificquiz with {number} questions on {topic} at {difficulty} difficulty. Format each question EXACTLY as follows:

**1. Question text**
A) Option A
B) Option B
C) Option C
D) Option D
Correct Answer: **[Single letter A, B, C, or D]**

Make sure to include the "Correct Answer:" line for each question, followed by a single letter (A, B, C, or D) corresponding to the correct option.
"""

print(generate_quiz(quiz_prompt, difficulty))

# Display all questions
print("\nAll questions in the database:")
for question in get_all_questions():
    print(f"ID: {question[0]}")
    print(f"Question: {question[1]}")
    print(f"A) {question[2]}")
    print(f"B) {question[3]}")
    print(f"C) {question[4]}")
    print(f"D) {question[5]}")
    print(f"Correct Answer: {question[6]}")
    print(f"Difficulty: {question[7]}")
    print(f"status: {question[8]}")

    print("------------------------")

#example input
'''
topic = "biomolecules"
difficulty = "medium"
number= "5"
'''
if __name__ == "__main__":
    # Ensure all arguments are passed
    if len(sys.argv) != 4:
        print(json.dumps({"error": "Incorrect number of arguments"}))
        sys.exit(1)
    
    try:
        topic = sys.argv[1]
        difficulty = sys.argv[2]
        number = sys.argv[3]
        
        # Generate quiz
        quiz_questions = generate_quiz(topic, difficulty, number)
        
        # Print as JSON for Node.js to parse
        print(json.dumps(quiz_questions))
    
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
# Close the connection
conn.close()

