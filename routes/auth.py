from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from models import User, WorkerProfile
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role', 'client') # Default to client if not specified
    
    if request.method == 'POST':
        # Special Admin Login Logic
        if role == 'admin':
            password = request.form.get('password')
            if password == "shahzad2005":
                # Find the admin user to log them in
                user = User.query.filter_by(role='admin').first()
                if user:
                    login_user(user)
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash('Error: No admin account found in database.')
            else:
                flash('Invalid Admin Password.')
            return render_template('login.html', role=role)

        # Normal Client/Worker Login
        email = request.form.get('email')
        password = request.form.get('password')
        # In a real app, we should also check if the user HAS this role
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # Redirect based on user's actual role, ensuring they go to the right place
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'worker':
                return redirect(url_for('worker.dashboard'))
            else:
                return redirect(url_for('client.dashboard'))
        else:
            flash('Login failed. Check your email and password.')
            
    return render_template('login.html', role=role)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    role = request.args.get('role', 'client')
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('auth.register', role=role))
            
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, phone=phone, password_hash=hashed_password, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        # If worker, create profile pending approval
        if role == 'worker':
            service = request.form.get('service')
            exp = request.form.get('experience')
            # For demo, random location or 0,0
            new_profile = WorkerProfile(user_id=new_user.id, service_category=service, experience_years=exp, location_lat=0, location_lon=0)
            db.session.add(new_profile)
            db.session.commit()
            flash('Registration successful! Please wait for admin approval.')
            return redirect(url_for('auth.login', role='worker'))
        
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login', role='client'))

    return render_template('register.html', role=role) 

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
