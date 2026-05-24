import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os
import json

# Ensure saved_models directory exists
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'saved_models'))
os.makedirs(MODEL_DIR, exist_ok=True)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'data'))
os.makedirs(DATA_DIR, exist_ok=True)

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    data = {
        'coding_skills': np.random.uniform(50, 100, num_samples),
        'aptitude_score': np.random.uniform(50, 100, num_samples),
        'attendance': np.random.uniform(50, 100, num_samples),
        'communication': np.random.uniform(50, 100, num_samples),
        'behavior': np.random.uniform(50, 100, num_samples),
        'cgpa': np.random.uniform(6.0, 10.0, num_samples)
    }
    df = pd.DataFrame(data)
    
    # Target 1: Performance Score (Linear Regression)
    # Roughly a weighted average
    df['performance_score'] = (
        df['coding_skills']*0.3 + 
        df['aptitude_score']*0.2 + 
        df['attendance']*0.1 + 
        df['communication']*0.15 + 
        df['behavior']*0.05 + 
        (df['cgpa']*10)*0.2
    )
    
    # Target 2: Placement Eligibility (Logistic Regression)
    # Eligible if score > 75 and CGPA > 7.5
    df['is_eligible'] = ((df['performance_score'] > 75) & (df['cgpa'] >= 7.5)).astype(int)
    
    return df

def generate_resume_data():
    # SVM, Decision Tree, Random Forest for Career Domain
    careers = [
        "Data Science", "Web Development", "AI/ML", 
        "Cybersecurity", "Cloud Computing", "Full Stack Development", 
        "UI/UX", "DevOps"
    ]
    
    keywords_map = {
        "Data Science": ["python", "pandas", "numpy", "sql", "machine learning", "statistics"],
        "Web Development": ["html", "css", "javascript", "react", "node", "frontend"],
        "AI/ML": ["tensorflow", "keras", "deep learning", "neural networks", "nlp", "computer vision"],
        "Cybersecurity": ["network", "security", "encryption", "firewall", "hacking", "linux"],
        "Cloud Computing": ["aws", "azure", "docker", "kubernetes", "cloud", "deployment"],
        "Full Stack Development": ["react", "node", "express", "mongodb", "api", "database"],
        "UI/UX": ["figma", "design", "wireframe", "prototype", "user experience", "adobe"],
        "DevOps": ["jenkins", "ci/cd", "linux", "bash", "docker", "terraform"]
    }
    
    # Save keywords for later
    with open(os.path.join(DATA_DIR, 'career_keywords.json'), 'w') as f:
        json.dump(keywords_map, f)
        
    X_text = []
    y_label = []
    
    import random
    random.seed(42)
    for _ in range(500):
        domain = random.choice(careers)
        num_words = random.randint(3, 6)
        words = random.sample(keywords_map[domain], num_words)
        # add some noise
        if random.random() > 0.5:
            other_domain = random.choice(careers)
            words.append(random.choice(keywords_map[other_domain]))
            
        X_text.append(" ".join(words))
        y_label.append(domain)
        
    return X_text, y_label

def train_all_models():
    print("Generating synthetic student data...")
    df = generate_synthetic_data()
    
    # 1. Linear Regression (Performance Score)
    X_reg = df[['coding_skills', 'aptitude_score', 'attendance', 'communication', 'behavior', 'cgpa']]
    y_reg = df['performance_score']
    
    lr_model = LinearRegression()
    lr_model.fit(X_reg, y_reg)
    joblib.dump(lr_model, os.path.join(MODEL_DIR, 'linear_regression.pkl'))
    print("Saved Linear Regression model.")
    
    # 2. Logistic Regression (Placement Eligibility)
    X_clf = df[['performance_score', 'cgpa']]
    y_clf = df['is_eligible']
    
    log_reg = LogisticRegression()
    log_reg.fit(X_clf, y_clf)
    joblib.dump(log_reg, os.path.join(MODEL_DIR, 'logistic_regression.pkl'))
    print("Saved Logistic Regression model.")
    
    # 3. KMeans Clustering (Batch Grouping as requested, even though rule-based was suggested)
    # We will cluster students based on overall performance features
    kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
    kmeans.fit(X_reg)
    joblib.dump(kmeans, os.path.join(MODEL_DIR, 'kmeans_clustering.pkl'))
    print("Saved KMeans model.")
    
    # Generate NLP Data
    X_text, y_label = generate_resume_data()
    vectorizer = TfidfVectorizer()
    X_tfidf = vectorizer.fit_transform(X_text)
    
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'))
    
    # 4. SVM (Career Domain)
    svm_model = SVC(probability=True, kernel='linear')
    svm_model.fit(X_tfidf, y_label)
    joblib.dump(svm_model, os.path.join(MODEL_DIR, 'svm_classifier.pkl'))
    print("Saved SVM model.")
    
    # 5. Decision Tree (Alternative Career Domain or just to include it)
    dt_model = DecisionTreeClassifier(max_depth=10)
    dt_model.fit(X_tfidf, y_label)
    joblib.dump(dt_model, os.path.join(MODEL_DIR, 'decision_tree.pkl'))
    print("Saved Decision Tree model.")
    
    # 6. Random Forest (Alternative Career Domain)
    rf_model = RandomForestClassifier(n_estimators=100)
    rf_model.fit(X_tfidf, y_label)
    joblib.dump(rf_model, os.path.join(MODEL_DIR, 'random_forest.pkl'))
    print("Saved Random Forest model.")

if __name__ == '__main__':
    train_all_models()
    print("All models trained and saved successfully.")
