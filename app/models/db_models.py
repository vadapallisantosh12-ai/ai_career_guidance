from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class StudentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    coding_skills = db.Column(db.Float)
    aptitude_score = db.Column(db.Float)
    attendance = db.Column(db.Float)
    communication = db.Column(db.Float)
    behavior = db.Column(db.Float)
    cgpa = db.Column(db.Float)
    
    # Predictions
    predicted_score = db.Column(db.Float)
    is_eligible = db.Column(db.Boolean)
    placement_probability = db.Column(db.Float)
    recommended_domain = db.Column(db.String(100))
    batch = db.Column(db.String(20))
    weak_areas = db.Column(db.String(200))
