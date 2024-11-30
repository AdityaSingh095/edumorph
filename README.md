## EduMorph - Personalized Learning Roadmap and Quiz Generator

**Project Overview**

EduMorph is a dynamic learning tool that empowers you to create personalized roadmaps and quizzes for your unique study goals.

**Key Features**

* **User Input Driven:** EduMorph starts by gathering your input on your learning objectives and current skill level.
* **Roadmap Generation:** Based on your input, EduMorph creates a custom roadmap outlining a structured learning path to achieve your goals.
* **Adaptive Quizzes:** EduMorph generates quizzes tailored to your current proficiency, offering targeted practice to reinforce your understanding.
* **Proficiency Tracking:** Your performance on quizzes continuously updates your proficiency level, allowing EduMorph to adjust your roadmap and quizzes accordingly.

**Project Structure**

EduMorph is organized into the following directories:

  - **backend:** Contains server-side code for handling user interactions and logic.
      - `server.js`: Main entry point for the backend server.
      - `routes/`: Houses route handlers for specific functionalities.
          - `roadmap.js`: Handles logic for generating personalized roadmaps.
          - `quiz.js`: Manages quiz generation and proficiency updates.
          - `proficiency.js`: Handles calculations and updates related to proficiency levels.
      - `utils/`: Utility functions used throughout the project.
          - `pythonRunner.js`: Handles communication with Python scripts.
  - **frontend:** Contains user interface code for interacting with the application.
      - `index.html`: Main HTML document for the user interface.
      - `styles.css`: Stylesheet for styling the user interface.
      - `app.js`: Frontend logic for user interaction and data exchange with the backend.
  - **python_scripts/`: Contains Python scripts for generating content.
      - `proficiency.py`: Logic for calculating proficiency levels based on quiz results.
      - `roadmap.py`: Implements the algorithm for creating personalized roadmaps.
      - `quizgen.py`: Generates quizzes based on the user's current proficiency.
  - **databases/`: Stores the data used by the application.
      - `study_plans.db`: Database for storing user-specific study plans.
      - `quiz.db`: Database for storing quiz questions and answers.
  - **package.json**: Manages dependencies required by the project.
  - **requirements.txt**: (Optional) Lists Python dependencies for development.

**Getting Started**

### Prerequisites

* Node.js and npm (or yarn)
* Python 3.x (for generating content with Python scripts)

### Installation

1. Clone this repository: `git clone https://github.com/your-username/eduMorph.git`
2. Navigate to the project directory: `cd eduMorph`
3. Install Node.js dependencies: `npm install`
4. (Optional) If using Python scripts: `pip install -r requirements.txt` (Adjust if using a different package manager)

### Run the Application

1. Start the backend server: `node server.js`
2. Access the application in your browser (usually at `http://localhost:3000` by default).

**How to Contribute**

We welcome contributions to improve EduMorph! Please consider the following guidelines before submitting a pull request:

  * Fork the repository and create a new branch for your changes.
  * Follow consistent code style and formatting.
  * Add unit tests for any new code or significant modifications.
  * Include clear documentation for any code changes.
  * Open a pull request to propose your changes.


**Additional Notes**

  * For more detailed documentation, refer to the individual code files and comments within the project.
  * Feel free to customize the styling and content of the frontend (`index.html` and `styles.css`) to match your preferences.
