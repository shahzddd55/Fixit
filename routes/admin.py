from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, WorkerProfile, Booking, db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def require_admin():
    if current_user.role != 'admin':
        return "Access Denied", 403

@admin_bp.route('/dashboard')
def dashboard():
    pending_workers = WorkerProfile.query.filter_by(is_approved=False).all()
    total_users = User.query.count()
    total_bookings = Booking.query.count()
    
    return render_template('admin/dashboard.html', 
                           pending_workers=pending_workers,
                           total_users=total_users,
                           total_bookings=total_bookings)

@admin_bp.route('/approve/<int:worker_id>')
def approve_worker(worker_id):
    worker = WorkerProfile.query.get_or_404(worker_id)
    worker.is_approved = True
    db.session.commit()
    flash(f'Worker {worker.user.name} approved!')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reject/<int:worker_id>')
def reject_worker(worker_id):
    worker = WorkerProfile.query.get_or_404(worker_id)
    # logic to delete or mark rejected
    db.session.delete(worker)
    # Also delete user? Just profile for now
    db.session.commit()
    flash('Worker application rejected.')
    return redirect(url_for('admin.dashboard'))

