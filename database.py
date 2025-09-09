import sqlite3
import os
from werkzeug.security import generate_password_hash

def get_db_path():
    return os.path.join(os.path.dirname(__file__), 'instance', 'healthcare.db')

def get_db():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(os.path.dirname(get_db_path())):
        os.makedirs(os.path.dirname(get_db_path()))
    
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    
    # Create patients table
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create doctors table
    c.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            hospital TEXT NOT NULL,
            experience INTEGER,
            rating REAL,
            image_url TEXT
        )
    ''')
    
    # Create medical_facilities table
    c.execute('''
        CREATE TABLE IF NOT EXISTS medical_facilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            phone TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    
    # Create appointments table
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (doctor_id) REFERENCES doctors (id)
        )
    ''')
    
    # Insert sample doctors
    sample_doctors = [
        ('Dr. Sarah Johnson', 'cardiology', 'City General Hospital', 15, 4.8, '/static/images/doctor1.jpg'),
        ('Dr. Michael Chen', 'dermatology', 'Skin Care Clinic', 10, 4.7, '/static/images/doctor2.jpg'),
        ('Dr. Emily Rodriguez', 'neurology', 'Neuro Center', 12, 4.9, '/static/images/doctor3.jpg'),
        ('Dr. James Wilson', 'pediatrics', 'Children\'s Hospital', 8, 4.6, '/static/images/doctor4.jpg'),
        ('Dr. Lisa Brown', 'orthopedics', 'Bone & Joint Institute', 18, 4.8, '/static/images/doctor5.jpg'),
        ('Dr. Robert Taylor', 'general', 'Community Health Center', 20, 4.5, '/static/images/doctor6.jpg')
    ]
    
    c.executemany('''
        INSERT OR IGNORE INTO doctors (name, specialty, hospital, experience, rating, image_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_doctors)
    
    # Insert sample medical facilities
    sample_facilities = [
        ('City General Hospital', 'hospital', '123 Healthcare Ave', 'Anytown', '(555) 123-4567', 40.7128, -74.0060),
        ('Community Health Clinic', 'clinic', '456 Wellness St', 'Anytown', '(555) 987-6543', 40.7138, -74.0070),
        ('QuickCare Pharmacy', 'pharmacy', '789 Medicine Rd', 'Anytown', '(555) 456-7890', 40.7148, -74.0080),
        ('Anytown Medical Center', 'hospital', '321 Doctor Ln', 'Anytown', '(555) 234-5678', 40.7158, -74.0090),
        ('Urgent Care Clinic', 'clinic', '654 Emergency Blvd', 'Anytown', '(555) 876-5432', 40.7168, -74.0100)
    ]
    
    c.executemany('''
        INSERT OR IGNORE INTO medical_facilities (name, type, address, city, phone, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_facilities)
    
    # Create a default user for testing
    hashed_password = generate_password_hash('password123')
    c.execute('''
        INSERT OR IGNORE INTO patients (username, password, email, full_name)
        VALUES (?, ?, ?, ?)
    ''', ('testuser', hashed_password, 'test@example.com', 'Test User'))
    
    conn.commit()
    conn.close()