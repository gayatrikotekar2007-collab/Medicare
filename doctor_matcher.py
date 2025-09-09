from database import get_db

def get_doctors_by_specialty(specialty):
    db = get_db()
    if specialty == 'all' or not specialty:
        doctors = db.execute('SELECT * FROM doctors').fetchall()
    else:
        doctors = db.execute(
            'SELECT * FROM doctors WHERE specialty = ?', (specialty,)
        ).fetchall()
    
    return [dict(doctor) for doctor in doctors]

def get_all_doctors():
    return get_doctors_by_specialty('all')

def get_doctor_by_id(doctor_id):
    db = get_db()
    doctor = db.execute(
        'SELECT * FROM doctors WHERE id = ?', (doctor_id,)
    ).fetchone()
    
    return dict(doctor) if doctor else None