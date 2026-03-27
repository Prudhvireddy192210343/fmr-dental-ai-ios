from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import User, DoctorProfile, Case, AppNotification
import bcrypt
import traceback
import os
import json
from datetime import datetime
from ai_engine import ai_engine
from feature_config import FEATURE_COLUMNS
from dotenv import load_dotenv

# Load production configurations
load_dotenv()

app = Flask(__name__)

# Security: CORS configuration
# In production, replace '*' with your frontend URL (e.g., 'https://fmr-ai.com')
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Configuration (from .env)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": ai_engine.model is not None}), 200

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        mobile = data.get('mobile')
        role = data.get('role', 'Doctor')

        if not all([name, email, password]):
            print(f"Missing fields: name={bool(name)}, email={bool(email)}, password={bool(password)}")
            return jsonify({"error": "Name, email, and password are required"}), 400

        if len(password) < 8:
            print(f"Password too short: {len(password)} chars")
            return jsonify({"error": "Password must be at least 8 characters long"}), 400

        if '@' not in email:
            print(f"Invalid email: {email}")
            return jsonify({"error": "Invalid email address"}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"Email already registered: {email}")
            return jsonify({"error": "Email already registered"}), 400

        # Hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        new_user = User(
            name=name,
            email=email,
            password_hash=hashed,
            mobile=mobile,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()
        
        # Create DoctorProfile automatically
        specialty = data.get('specialty', 'Select specialty')
        experience = data.get('yearsOfExperience', '')
        clinic = data.get('clinicName', '')
        
        new_profile = DoctorProfile(
            user_id=new_user.id,
            fullName=name,
            selectedSpecialty=specialty,
            yearsOfExperience=experience,
            clinicName=clinic,
            profileImageUrl=None
        )
        db.session.add(new_profile)
        db.session.commit()

        return jsonify({"message": "Successfully registered", "id": new_user.id}), 201
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
            
        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return jsonify({"message": "success", "user_id": str(user.id), "name": user.name}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route('/cases', methods=['GET', 'POST'])
def handle_cases():
    try:
        if request.method == 'GET':
            cases = Case.query.order_by(Case.createdDate.desc()).all()
            return jsonify([{
                "id": c.id,
                "patientName": c.patientName,
                "patientId": c.patientId,
                "patientImageUrl": c.patientImageUrl,
                "chiefComplaint": c.chiefComplaint,
                "complaintType": c.complaintType,
                "additionalDetails": c.additionalDetails,
                "medicalHistory": c.medicalHistory,
                "status": c.status,
                "createdDate": c.createdDate.isoformat() if c.createdDate else None,
                "lastUpdated": c.lastUpdated.isoformat() if c.lastUpdated else None,
                "doctorId": c.doctorId,
                "doctorName": c.doctorName,
                "clinicalFeatures": c.clinicalFeatures,
                "lastAIResult": c.lastAIResult,
                "patientAge": c.patientAge,
                "patientGender": c.patientGender
            } for c in cases]), 200
            
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid request"}), 400
            
            new_case = Case(
                id=data.get('id'),
                patientName=data.get('patientName'),
                patientId=data.get('patientId'),
                patientImageUrl=data.get('patientImageUrl'),
                chiefComplaint=data.get('chiefComplaint'),
                complaintType=data.get('complaintType'),
                additionalDetails=data.get('additionalDetails'),
                medicalHistory=data.get('medicalHistory'),
                patientAge=data.get('patientAge'),
                patientGender=data.get('patientGender'),
                status=data.get('status', 'active'),
                doctorId=data.get('doctorId', 'DR001'),
                doctorName=data.get('doctorName', 'Doctor'),
                clinicalFeatures=data.get('clinicalFeatures', {}),
                lastAIResult=data.get('lastAIResult', {})
            )
            db.session.add(new_case)
            db.session.commit()
            return jsonify(data), 201
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/cases/<id>', methods=['PUT', 'DELETE'])
def handle_single_case(id):
    try:
        case_item = Case.query.get(id)
        if not case_item:
            return jsonify({"error": "Case not found"}), 404
            
        if request.method == 'PUT':
            data = request.get_json()
            case_item.patientName = data.get('patientName', case_item.patientName)
            case_item.status = data.get('status', case_item.status)
            case_item.lastUpdated = datetime.utcnow()
            case_item.clinicalFeatures = data.get('clinicalFeatures', case_item.clinicalFeatures)
            case_item.lastAIResult = data.get('lastAIResult', case_item.lastAIResult)
            
            db.session.commit()
            return jsonify(data), 200
            
        elif request.method == 'DELETE':
            db.session.delete(case_item)
            db.session.commit()
            return jsonify({"message": "Deleted successfully"}), 200
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/notifications', methods=['GET', 'POST', 'DELETE'])
def handle_notifications():
    try:
        if request.method == 'GET':
            notifications = AppNotification.query.order_by(AppNotification.timestamp.desc()).all()
            return jsonify([{
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "timestamp": n.timestamp.isoformat() if n.timestamp else None,
                "isNew": n.isNew
            } for n in notifications]), 200
            
        elif request.method == 'POST':
            data = request.get_json()
            new_notif = AppNotification(
                id=data.get('id'),
                title=data.get('title'),
                message=data.get('message'),
                isNew=data.get('isNew', True)
            )
            db.session.add(new_notif)
            db.session.commit()
            return jsonify(data), 201
            
        elif request.method == 'DELETE':
            AppNotification.query.delete()
            db.session.commit()
            return jsonify({"message": "Cleared all notifications"}), 200
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/profile', methods=['GET', 'PUT'])
def handle_profile():
    try:
        email = request.args.get('email')
        user = User.query.filter_by(email=email).first() if email else None
        user_id = user.id if user else None
        
        if user_id:
            profile = DoctorProfile.query.filter_by(user_id=user_id).first()
        else:
            profile = DoctorProfile.query.first()
            
        if request.method == 'GET':
            if not profile:
                default_name = user.name if user else "Doctor"
                return jsonify({"id": 0, "fullName": default_name, "selectedSpecialty": "Select specialty", "profileImageUrl": None}), 200
            
            return jsonify({
                "id": profile.id,
                "fullName": profile.fullName,
                "selectedSpecialty": profile.selectedSpecialty,
                "yearsOfExperience": profile.yearsOfExperience,
                "clinicName": profile.clinicName,
                "profileImageUrl": profile.profileImageUrl
            }), 200
            
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid request"}), 400
            
            print(f"Updating profile with data: {data} for user_id: {user_id}")
                
            if not profile:
                profile = DoctorProfile(
                    user_id=user_id,
                    fullName=data.get('fullName', ''),
                    selectedSpecialty=data.get('selectedSpecialty', 'Select specialty'),
                    yearsOfExperience=data.get('yearsOfExperience'),
                    clinicName=data.get('clinicName'),
                    profileImageUrl=data.get('profileImageUrl')
                )
                db.session.add(profile)
            else:
                profile.fullName = data.get('fullName', profile.fullName)
                profile.selectedSpecialty = data.get('selectedSpecialty', profile.selectedSpecialty)
                profile.yearsOfExperience = data.get('yearsOfExperience', profile.yearsOfExperience)
                profile.clinicName = data.get('clinicName', profile.clinicName)
                profile.profileImageUrl = data.get('profileImageUrl', profile.profileImageUrl)
                if user_id and not profile.user_id:
                    profile.user_id = user_id
                    
            if user and 'fullName' in data:
                user.name = data['fullName']
                
            db.session.commit()
            print(f"Profile updated successfully for: {profile.fullName}")
            
            return jsonify({
                "id": profile.id,
                "fullName": profile.fullName,
                "selectedSpecialty": profile.selectedSpecialty,
                "yearsOfExperience": profile.yearsOfExperience,
                "clinicName": profile.clinicName,
                "profileImageUrl": profile.profileImageUrl
            }), 200
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@app.route('/check-email', methods=['POST'])
def check_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400
        
        email = data.get('email')
        if not email:
            return jsonify({"error": "Email is required"}), 400
            
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"message": "User exists"}), 200
        else:
            return jsonify({"error": "Email not registered"}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400
            
        email = data.get('email')
        new_password = data.get('new_password')
        
        if not email or not new_password:
            return jsonify({"error": "Email and new password are required"}), 400
            
        if len(new_password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
            
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Hash new password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), salt).decode('utf-8')
        
        user.password_hash = hashed
        db.session.commit()
        
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Check if image is present
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        image_file = request.files['image']
        
        # 2. Extract clinical features
        features_str = request.form.get('features')
        if not features_str:
            print("No features provided in the request form")
            return jsonify({"error": "No clinical features provided"}), 400
            
        try:
            features_dict = json.loads(features_str)
            # Ensure features are in the correct order for the model
            # Use data.get(k) or 0 to handle explicit nulls or missing keys
            ordered_features = [float(features_dict.get(col) or 0) for col in FEATURE_COLUMNS]
            print(f"Extracted features for analysis: {ordered_features}")
        except Exception as e:
            print(f"Features extraction error: {e}")
            return jsonify({"error": f"Invalid features format: {str(e)}"}), 400

        # 3. Run AI prediction
        results = ai_engine.predict(image_file, ordered_features)
        
        if "error" in results:
            return jsonify(results), 500

        return jsonify(results), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    # In production, set debug to False
    app.run(debug=False, host='0.0.0.0', port=port)
