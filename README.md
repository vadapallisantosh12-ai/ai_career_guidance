<<<<<<< HEAD
# AI Career Guidance System

This is a complete AI Career Guidance System built with Flask and Scikit-Learn.

## Architecture

- **Frontend:** HTML, CSS, Bootstrap 5, Chart.js.
- **Backend:** Python (Flask), SQLAlchemy.
- **Machine Learning Models:**
  - **Linear Regression:** Predicts overall performance score based on student metrics.
  - **Logistic Regression:** Classifies placement eligibility based on predicted score and CGPA.
  - **Support Vector Machine (SVM):** Classifies the career domain from resume keywords (TF-IDF vectorization).
  - **Decision Tree / Random Forest:** Alternative models included in the training script for comparison.
  - **K-Means Clustering:** Clusters students into batches based on performance.
- **Resume Parsing:** Uses PyMuPDF (fitz) to extract text from uploaded resumes and compares against a skills keyword map.

## Project Structure
```text
ai_career_guidance/
├── app/
│   ├── routes/          # Flask blueprints (auth, student, admin)
│   ├── models/          # SQLAlchemy db_models & Scikit-learn ml_models
│   ├── services/        # Resume parsing logic
│   ├── templates/       # HTML templates matching UI designs
│   └── static/css/      # Custom styles
├── data/                # Generated sample data & career keywords map
├── saved_models/        # Serialized scikit-learn (.pkl) models
├── config.py            # App config
├── requirements.txt     # Dependencies
└── run.py               # Application entry point
```

## How to Run

1. **Activate Virtual Environment & Install Requirements**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Train the ML Models**
   Before running the app, generate the synthetic training data and train the Scikit-Learn models.
   ```bash
   python app/models/ml_models/train_models.py
   ```
   *This will save the `.pkl` files in the `saved_models` directory.*

3. **Run the Application**
   ```bash
   python run.py
   ```
   *The server will start at `http://127.0.0.1:5000`.*

## Features Implemented
- **Login / Register UI:** Matches the dark green UI requested.
- **Upload Resume UI:** A dedicated route for uploading files (`/upload`).
- **Student Form:** A form to collect Coding Skills, Aptitude, etc.
- **AI Analytics Results:** Shows Resume Score, Placement Eligibility, Extracted Skills, and Recommended Career Domain (matches the requested result dashboard).
- **Admin Dashboard:** Visualizes batches and student states using Chart.js.
=======
# ai_career_guidance
>>>>>>> 1b5a9a6d79e2742d653067d393236845b5665b9b
