from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename
import os
from app.models.ml_models.predict import predict_all

student_bp = Blueprint('student', __name__)

@student_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@student_bp.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if request.method == 'POST':
        data = {
            'coding_skills': float(request.form.get('coding_skills')),
            'aptitude_score': float(request.form.get('aptitude_score')),
            'attendance': float(request.form.get('attendance')),
            'communication': float(request.form.get('communication')),
            'behavior': float(request.form.get('behavior')),
            'cgpa': float(request.form.get('cgpa'))
        }
        
        # We need to handle file upload for resume
        if 'resume' not in request.files:
            flash('No resume part')
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        resume_path = ""
        if file:
            filename = secure_filename(file.filename)
            resume_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(resume_path)
            
        # Run ML predictions
        results = predict_all(data, resume_path)
        
        return render_template('resume_result.html', results=results, data=data)
        
    return render_template('student_form.html')

@student_bp.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload_resume.html')
