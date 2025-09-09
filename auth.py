from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

def register_user(username, password, email, full_name):
    db = get_db()
    
    # Check if username already exists
    existing_user = db.execute(
        'SELECT id FROM patients WHERE username = ?', (username,)
    ).fetchone()
    
    if existing_user:
        return False
    
    # Hash password and insert new user
    hashed_password = generate_password_hash(password)
    db.execute(
        'INSERT INTO patients (username, password, email, full_name) VALUES (?, ?, ?, ?)',
        (username, hashed_password, email, full_name)
    )
    db.commit()
    return True

def login_user(username, password):
    db = get_db()
    user = db.execute(
        'SELECT * FROM patients WHERE username = ?', (username,)
    ).fetchone()
    
    if user and check_password_hash(user['password'], password):
        return dict(user)
    return None