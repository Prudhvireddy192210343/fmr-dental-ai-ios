from main import app, db
from models import Case

with app.app_context():
    cases = Case.query.all()
    print(f"Total cases: {len(cases)}")
    for c in cases:
        print(f"ID: {c.id}, Patient: {c.patientName}, Doctor: {c.doctorName}")
