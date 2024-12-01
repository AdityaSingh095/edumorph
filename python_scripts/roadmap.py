from google.colab import userdata
import google.generativeai as genai
import sqlite3
import ast
import json
import sys

genai.configure(api_key='Your API Key')
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Connect to the SQLite database
conn = sqlite3.connect("study_plans.db")
cursor = conn.cursor()
def generate_and_store_study_plan(topic, duration):
    # Create the table for the given topic if it doesn't exist
    table_name = topic.replace(" ", "_")  # Replace spaces with underscores for table name
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS '{table_name}' (
            subtopic TEXT,
            description TEXT,
            study_material TEXT,
            time_to_be_given TEXT,
            proficiency INTEGER DEFAULT 0
        )
    """)

    # Generate the study plan using the Generative AI model
    prompt = f"Generate a JEE specific roadmap for the topic of {topic} over a duration of {duration}. Generate it in the format [[subtopic1,short description with no comma written in text(content should remain between these commas. no other comma should be there bwtween these commas), suggected study material with no commas written in text (content should remain between these commas. no other comma to be written b/w these commas),time to be given],[subtopic2, ...]...]. dont make a week wise plan .stick to the format provided earlier strictly.provideed answer should only be in the given format no other text or word to be written."
    response = model.generate_content(prompt)
    generated_plan = response.text
    print(generated_plan)

    # Parse the generated plan and store it in the table
    plan_items = []
    for item in generated_plan.strip('[]').split('],'):
        subtopic_time = [part.strip() for part in item.split(',')]
        subtopic = subtopic_time[0].strip('"')
        description= subtopic_time[1].strip('"')
        study_material = subtopic_time[2].strip('"')
        time_to_be_given = subtopic_time[3].strip('"')

        plan_items.append((subtopic, description, study_material, time_to_be_given))

    for subtopic, description, study_material, time_to_be_given in plan_items:
        cursor.execute(f"""
            INSERT INTO '{table_name}' (subtopic, description, study_material, time_to_be_given)
            VALUES (?, ?, ?, ?)
        """, (subtopic, description, study_material, time_to_be_given))
    conn.commit()

    return 0



'''
# Print the generated table
print("\nGenerated Study Plan Table:")
topic_name = topic.replace(" ", "_")
cursor.execute(f"SELECT * FROM {topic_name}")
rows = cursor.fetchall()
for row in rows:
    print(f"Subtopic: {row[0]}, description: {row[1]}, material: {row[2]}, time_to_be_given: {row[3]} Proficiency: {row[4]}")
'''
if __name__ == "__main__":
    # Ensure all arguments are passed
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Incorrect number of arguments"}))
        sys.exit(1)
    
    try:
        topic = sys.argv[1]
        duration = sys.argv[2]
        
        # Generate quiz
        generate_and_store_study_plan(topic, duration)
               
    
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


# Close the database connection
conn.close()
