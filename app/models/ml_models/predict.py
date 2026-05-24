import os
import joblib
import pandas as pd
import json
from app.services.resume_parser import extract_text_from_pdf

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'saved_models'))

# Load models safely (they might not exist if train_models.py hasn't been run)
def load_model(name):
    path = os.path.join(MODEL_DIR, name)
    if os.path.exists(path):
        return joblib.load(path)
    return None

def predict_all(student_data, resume_path=None):
    lr_model = load_model('linear_regression.pkl')
    log_reg = load_model('logistic_regression.pkl')
    svm_model = load_model('svm_classifier.pkl')
    vectorizer = load_model('tfidf_vectorizer.pkl')
    
    # 1. Performance Score Prediction
    X_reg = pd.DataFrame([{
        'coding_skills': student_data['coding_skills'],
        'aptitude_score': student_data['aptitude_score'],
        'attendance': student_data['attendance'],
        'communication': student_data['communication'],
        'behavior': student_data['behavior'],
        'cgpa': student_data['cgpa']
    }])
    
    perf_score = 0
    if lr_model:
        perf_score = lr_model.predict(X_reg)[0]
        # Keep score in 0-100 range logically
        perf_score = max(0, min(100, perf_score))
    else:
        # Fallback if model not trained
        perf_score = 75.0
        
    # 2. Eligibility Prediction
    eligibility = "Not Eligible"
    prob = 0.0
    if log_reg:
        X_clf = pd.DataFrame([{'performance_score': perf_score, 'cgpa': student_data['cgpa']}])
        elig = log_reg.predict(X_clf)[0]
        prob = log_reg.predict_proba(X_clf)[0][1] * 100
        eligibility = "Eligible" if elig == 1 else "Not Eligible"
        
    # 3. Batch Assignment (Rule-based as requested)
    batch = "Improvement Batch"
    if perf_score >= 90:
        batch = "Batch A"
    elif perf_score >= 75:
        batch = "Batch B"
    elif perf_score >= 60:
        batch = "Batch C"
        
    # 4. Career Domain from Resume
    domain = "General IT"
    skills_extracted = []
    if resume_path and os.path.exists(resume_path) and svm_model and vectorizer:
        resume_text = extract_text_from_pdf(resume_path)
        X_tfidf = vectorizer.transform([resume_text])
        domain = svm_model.predict(X_tfidf)[0]
        
        # Extracted Skills mockup
        words = resume_text.lower().split()
        with open(os.path.join(MODEL_DIR, '../data/career_keywords.json'), 'r') as f:
            keywords_map = json.load(f)
        all_kw = []
        for klist in keywords_map.values():
            all_kw.extend(klist)
        skills_extracted = list(set([w for w in words if w in all_kw]))
        
    # 5. Weak Area Detection
    weak_areas = []
    if student_data['aptitude_score'] < 60: weak_areas.append("Aptitude")
    if student_data['communication'] < 60: weak_areas.append("Communication")
    if student_data['attendance'] < 75: weak_areas.append("Attendance")
    if student_data['coding_skills'] < 60: weak_areas.append("Coding")
    
    # 6. ATS Score & Suggestions
    ats_score = 0
    ats_suggestions = []
    
    if resume_path and os.path.exists(resume_path):
        # Calculate a basic ATS score based on word count and found keywords
        words_len = len(resume_text.split())
        keyword_match_ratio = len(skills_extracted) / max(1, len(all_kw)) * 100
        
        # Simple heuristic for dummy score
        ats_score = int(min(100, max(15, (words_len / 500 * 40) + (keyword_match_ratio * 2))))
        
        if len(skills_extracted) < 5:
            ats_suggestions.append("Add more industry-specific keywords and hard skills.")
        if words_len < 200:
            ats_suggestions.append("Your resume is too short. Elaborate on your projects and experience.")
        if "project" not in resume_text.lower():
            ats_suggestions.append("Include a clear 'Projects' section with quantifiable achievements.")
        if "education" not in resume_text.lower():
            ats_suggestions.append("Clearly highlight your 'Education' and graduation dates.")
        if not ats_suggestions:
            ats_suggestions.append("Great job! Consider using stronger action verbs to boost your score further.")
    else:
        ats_score = 15
        ats_suggestions = ["Please upload a valid PDF resume to get ATS insights."]

    return {
        'performance_score': round(perf_score, 2),
        'eligibility': eligibility,
        'placement_probability': round(prob, 2),
        'batch': batch,
        'career_domain': domain,
        'extracted_skills': skills_extracted[:10], # Top 10
        'weak_areas': weak_areas,
        'ats_score': ats_score,
        'ats_suggestions': ats_suggestions
    }
