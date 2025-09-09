from flask import Flask, render_template, redirect, url_for, session, request
from database import init_db, get_db
from auth import register_user, login_user
from doctor_matcher import get_doctors_by_specialty, get_all_doctors
from facility_finder import get_nearby_facilities
from appointment_handler import book_appointment, get_user_appointments
from remedies import get_remedies_for_symptom, get_all_remedies

app = Flask(__name__)
app.secret_key = '7fee8d10a5433f07f43ef100b68c14efcc192ec24c804902e1d9f4de3f5c3ffb'  # Change this in production

# Initialize database
init_db()

@app.route('/')
def index():
    # Always render the index.html template for the home page
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        full_name = request.form['full_name']
        
        if register_user(username, password, email, full_name):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    appointments = get_user_appointments(session['user_id'])
    return render_template('dashboard.html', 
                           username=session['username'], 
                           appointments=appointments)

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        # Simple keyword matching (in a real app, this would be more sophisticated)
        if 'heart' in symptoms.lower() or 'chest' in symptoms.lower():
            specialty = 'cardiology'
        elif 'skin' in symptoms.lower() or 'rash' in symptoms.lower():
            specialty = 'dermatology'
        elif 'headache' in symptoms.lower() or 'migraine' in symptoms.lower():
            specialty = 'neurology'
        else:
            specialty = 'general'
        
        doctors = get_doctors_by_specialty(specialty)
        return render_template('doctors.html', doctors=doctors, symptoms=symptoms)
    
    return render_template('symptoms.html')

@app.route('/doctors')
def doctors():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    specialty = request.args.get('specialty', '')
    if specialty:
        doctors = get_doctors_by_specialty(specialty)
    else:
        doctors = get_all_doctors()
    
    return render_template('doctors.html', doctors=doctors)

@app.route('/facilities')
def facilities():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    location = request.args.get('location', '')
    facility_type = request.args.get('type', '')
    
    facilities = get_nearby_facilities(location, facility_type)
    return render_template('facilities.html', facilities=facilities)

@app.route('/remedies', methods=['GET', 'POST'])
def remedies():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    symptom = request.args.get('symptom', '')
    remedies_data = None
    
    if request.method == 'POST':
        symptom = request.form['symptom']
        return redirect(url_for('remedies', symptom=symptom))
    
    if symptom:
        remedies_data = get_remedies_for_symptom(symptom)
    else:
        # Show all remedies if no specific symptom is provided
        remedies_data = get_all_remedies()
    
    return render_template('remedies.html', remedies=remedies_data, symptom=symptom)

# Health Tracking route
@app.route('/health_tracking')
def health_tracking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('health_tracking.html', username=session['username'])

# Chatbot route
@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('ChatBot.html', username=session['username'])

@app.route('/book_appointment', methods=['POST'])
def book_appointment_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    
    doctor_id = request.form['doctor_id']
    date = request.form['date']
    time = request.form['time']
    
    appointment_id = book_appointment(session['user_id'], doctor_id, date, time)
    if appointment_id:
        return redirect(url_for('confirmation', appointment_id=appointment_id))
    else:
        return redirect(url_for('doctors', error='Failed to book appointment'))

@app.route('/confirmation')
def confirmation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    appointment_id = request.args.get('appointment_id')
    db = get_db()
    appointment = db.execute(
        'SELECT a.*, d.name as doctor_name, d.specialty '
        'FROM appointments a JOIN doctors d ON a.doctor_id = d.id '
        'WHERE a.id = ?', (appointment_id,)
    ).fetchone()
    
    return render_template('confirmation.html', appointment=appointment)

# Health Resources routes
@app.route('/health_guides')
def health_guides():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('health_guides.html', username=session['username'])

@app.route('/healthy_recipes')
def healthy_recipes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('healthy_recipes.html', username=session['username'])

@app.route('/exercise_videos')
def exercise_videos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('exercise_videos.html', username=session['username'])



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)