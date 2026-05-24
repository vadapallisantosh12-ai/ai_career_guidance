from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # In a real app, we would verify if current_user.is_admin is true
    # and fetch statistics from the database.
    stats = {
        'total_students': 150,
        'eligible': 120,
        'not_eligible': 30,
        'batch_a': 45,
        'batch_b': 60,
        'batch_c': 45
    }
    return render_template('dashboard.html', stats=stats)
