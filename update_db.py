from main import app, db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE cases ADD COLUMN patientAge VARCHAR(20)"))
        db.session.execute(text("ALTER TABLE cases ADD COLUMN patientGender VARCHAR(20)"))
        db.session.commit()
        print("Columns added successfully")
    except Exception as e:
        print(f"Error adding columns: {e}")
