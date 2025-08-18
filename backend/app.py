from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io

app = Flask(__name__)
CORS(app)

students = []  # In-memory list

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

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500


@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)


@app.route("/students", methods=["POST"])
def add_student():
    try:
        data = request.json
        if not data.get("name") or not data.get("roll") or "marks" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        # Check for duplicate roll numbers
        if any(s["roll"] == data["roll"] for s in students):
            return jsonify({"error": "Roll number already exists"}), 400

        student = {
            "name": data["name"],
            "roll": str(data["roll"]),
            "marks": int(data["marks"]),
            "grade": calculate_grade(data["marks"])
        }
        students.append(student)
        return jsonify({"message": "Student added", "student": student}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/students/<roll>", methods=["PUT"])
def update_student(roll):
    try:
        data = request.json
        for student in students:
            if student["roll"] == roll:
                if not data.get("name") or "marks" not in data:
                    return jsonify({"error": "Missing required fields"}), 400
                student["name"] = data["name"]
                student["marks"] = int(data["marks"])
                student["grade"] = calculate_grade(data["marks"])
                return jsonify({"message": "Student updated", "student": student}), 200
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/export", methods=["GET"])
def export_csv():
    if not students:
        return jsonify({"error": "No students to export"}), 400
    df = pd.DataFrame(students)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="students.csv"
    )


if __name__ == "__main__":
    app.run(debug=True)
