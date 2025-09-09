from database import get_db

def book_appointment(patient_id, doctor_id, date, time):
    db = get_db()
    
    try:
        cursor = db.execute(
            'INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)',
            (patient_id, doctor_id, date, time)
        )
        db.commit()
        return cursor.lastrowid
    except:
        return None

def get_user_appointments(patient_id):
    db = get_db()
    appointments = db.execute(
        'SELECT a.*, d.name as doctor_name, d.specialty, d.hospital '
        'FROM appointments a JOIN doctors d ON a.doctor_id = d.id '
        'WHERE a.patient_id = ? ORDER BY a.date, a.time', (patient_id,)
    ).fetchall()
    
    return [dict(appt) for appt in appointments]