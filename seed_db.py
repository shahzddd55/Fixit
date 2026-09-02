from app import create_app
from extensions import db
from models import User, WorkerProfile
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    
    # Check if admin exists
    if not User.query.filter_by(email='admin@fixit.com').first():
        print("Creating Admin User...")
        admin = User(
            name='Super Admin',
            email='admin@fixit.com',
            phone='0000000000',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)

    # Check if a worker exists
    if not User.query.filter_by(email='plumber@fixit.com').first():
        print("Creating Approved Plumber...")
        plumber = User(
            name='Mario Bros',
            email='plumber@fixit.com',
            phone='9876543210',
            password_hash=generate_password_hash('worker123'),
            role='worker'
        )
        db.session.add(plumber)
        db.session.commit() # Commit user first to get ID
        
        p_profile = WorkerProfile(
            user_id=plumber.id,
            service_category='Plumber',
            experience_years=10,
            location_lat=10.0,
            location_lon=76.0,
            is_approved=True,
            rating=4.8
        )
        db.session.add(p_profile)

    # Creating a Pending Worker
    if not User.query.filter_by(email='electric@fixit.com').first():
        print("Creating Pending Electrician...")
        electric = User(
            name='Sparky',
            email='electric@fixit.com',
            phone='9876543211',
            password_hash=generate_password_hash('worker123'),
            role='worker'
        )
        db.session.add(electric)
        db.session.commit()
        
        e_profile = WorkerProfile(
            user_id=electric.id,
            service_category='Electrician',
            experience_years=3,
            location_lat=10.1,
            location_lon=76.1,
            is_approved=False
        )
        db.session.add(e_profile)

    # Create Client
    if not User.query.filter_by(email='client@fixit.com').first():
        print("Creating Test Client...")
        client = User(
            name='John Homeowner',
            email='client@fixit.com',
            phone='9999999999',
            password_hash=generate_password_hash('client123'),
            role='client'
        )
        db.session.add(client)

    db.session.commit()
    print("Database seeded successfully!")
