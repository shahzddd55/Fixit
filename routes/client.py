from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import WorkerProfile, Booking, db, User
import random

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('client/dashboard.html')

@client_bp.route('/service/<service_name>')
@login_required
def service_workers(service_name):
    # In a real app, we would use PostGIS or Haversine with user's lat/lon
    # Here we just fetch all approved workers of that category
    # And mock a distance for display
    workers = WorkerProfile.query.filter_by(service_category=service_name, is_approved=True).all()
    
    # Enrich with mock distance
    results = []
    for w in workers:
        # Distance calculation mock
        dist = round(random.uniform(0.5, 5.0), 1)
        results.append({
            'profile': w,
            'user': w.user,
            'distance': dist
        })
    
    # Sort by distance
    results.sort(key=lambda x: x['distance'])
    
    return render_template('client/workers_list.html', service=service_name, workers=results)

@client_bp.route('/book/<int:worker_id>', methods=['POST'])
@login_required
def book_worker(worker_id):
    worker_profile = WorkerProfile.query.get_or_404(worker_id)
    service = worker_profile.service_category
    
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    booking = Booking(
        client_id=current_user.id,
        worker_id=worker_profile.user_id,
        service_type=service,
        status='pending',
        verification_code=otp
    )
    
    db.session.add(booking)
    db.session.commit()
    
    flash('Booking sent! Waiting for worker acceptance.')
    return redirect(url_for('client.booking_success', booking_id=booking.id))

@client_bp.route('/booking-success/<int:booking_id>')
@login_required
def booking_success(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.client_id != current_user.id:
        return redirect(url_for('client.dashboard'))
    return render_template('client/booking_success.html', booking=booking)

