# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request

app = Flask(__name__)

students = [
    {"id": 1, "first_name": "John", "last_name": "Doe", "age": 21},
    {"id": 2, "first_name": "Jane", "last_name": "Smith", "age": 23}
]

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'age']
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400
    
    new_id = max([student['id'] for student in students], default=0) + 1
    new_student = {
        "id": new_id,
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "age": data['age']
    }
    students.append(new_student)
    return jsonify(new_student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'age']
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400
    
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    student['first_name'] = data['first_name']
    student['last_name'] = data['last_name']
    student['age'] = data['age']
    
    return jsonify(student), 200

@app.route('/students/<int:student_id>', methods=['PATCH'])
def patch_student_age(student_id):
    data = request.get_json()
    
    if not data or 'age' not in data:
        return jsonify({"error": "Missing age field"}), 400
    
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    student['age'] = data['age']
    return jsonify(student), 200

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    students = [s for s in students if s['id'] != student_id]
    return jsonify({"message": "Student deleted successfully"}), 200

@app.route('/students/all', methods=['DELETE'])
def delete_all_students():
    global students
    students = []
    return jsonify({"message": "All students deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)