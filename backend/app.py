from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io
import os
import time
import pymysql

# --------------------------
# Database connection info
# --------------------------
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "userpassword")
DB_NAME = os.getenv("DB_NAME", "mydatabase")

# Wait for MySQL to be ready
print("Waiting for MySQL to be ready...")
while True:
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        conn.close()
        print("MySQL is ready!")
        break
    except Exception:
        print("MySQL not ready yet, retrying in 2s...")
        time.sleep(2)

# --------------------------
# Flask app setup
# --------------------------
app = Flask(__name__)
CORS(app)

# SQLAlchemy configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --------------------------
# StudentRecord model
# --------------------------
class StudentRecord(db.Model):
    __tablename__ = "student_record"

    roll = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(2), nullable=False)

    def to_dict(self):
        return {
            "roll": self.roll,
            "name": self.name,
            "marks": self.marks,
            "grade": self.grade,
        }

# --------------------------
# Grade calculator
# --------------------------
def calculate_grade(marks: int):
    try:
        marks = int(marks)
        if marks >= 90:
            return "A"
        elif marks >= 75:
            return "B"
        elif marks >= 60:
            return "C"
        elif marks >= 40:
            return "D"
        else:
            return "F"
    except Exception:
        return "Invalid"

# --------------------------
# Error handling
# --------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

# --------------------------
# Routes
# --------------------------
@app.route("/students", methods=["GET"])
def get_students():
    students = StudentRecord.query.all()
    return jsonify([s.to_dict() for s in students])

@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    if not data.get("name") or not data.get("roll") or "marks" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if StudentRecord.query.filter_by(roll=str(data["roll"])).first():
        return jsonify({"error": "Roll number already exists"}), 400

    grade = calculate_grade(data["marks"])
    new_student = StudentRecord(
        roll=str(data["roll"]),
        name=data["name"],
        marks=int(data["marks"]),
        grade=grade
    )
    db.session.add(new_student)
    db.session.commit()

    return jsonify({"message": "Student added", "student": new_student.to_dict()}), 201

@app.route("/students/<roll>", methods=["PUT"])
def update_student(roll):
    data = request.json
    student = StudentRecord.query.filter_by(roll=roll).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    if not data.get("name") or "marks" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    student.name = data["name"]
    student.marks = int(data["marks"])
    student.grade = calculate_grade(student.marks)
    db.session.commit()

    return jsonify({"message": "Student updated", "student": student.to_dict()}), 200

@app.route("/export", methods=["GET"])
def export_csv():
    students = StudentRecord.query.all()
    if not students:
        return jsonify({"error": "No students to export"}), 400

    df = pd.DataFrame([s.to_dict() for s in students])
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="students.csv",
    )

# --------------------------
# Main
# --------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
