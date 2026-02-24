from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Temporary Storage
students_list = []
rooms_list = []
fees_list = []

# ================= LOGIN =================
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_input = request.form.get('login_input')
        password = request.form.get('password')

        if (login_input in ["admin", "admin@gmail.com", "9876543210"]) and password == "admin123":
            return redirect('/dashboard')
        else:
            error = "Invalid Username / Email / Phone or Password"

    return render_template("index.html", error=error)


# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    total_students = len(students_list)
    total_rooms = len(rooms_list)
    available_rooms = sum(1 for r in rooms_list if r["room_status"] == "Available")

    total_fees = sum(int(s["fees_amount"]) for s in students_list if s["fees_status"] == "Paid")
    pending_fees = sum(int(s["fees_amount"]) for s in students_list if s["fees_status"] == "Pending")

    return render_template("dashboard.html",
                           total_students=total_students,
                           total_rooms=total_rooms,
                           available_rooms=available_rooms,
                           total_fees=total_fees,
                           pending_fees=pending_fees)


# ================= STUDENTS =================
@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        students_list.append({
            "student_id": request.form.get('student_id'),
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "department": request.form.get('department'),
            "year": request.form.get('year'),
            "gender": request.form.get('gender'),
            "address": request.form.get('address'),
            "room": request.form.get('room'),
            "contact": request.form.get('contact'),
            "admission_date": request.form.get('admission_date'),
            "fees_amount": request.form.get('fees_amount'),
            "fees_status": request.form.get('fees_status')
        })
        return redirect('/students')

    return render_template("students.html", students=students_list)


@app.route('/delete_student/<student_id>')
def delete_student(student_id):
    global students_list
    students_list = [s for s in students_list if s["student_id"] != student_id]
    return redirect('/students')


@app.route('/edit_student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = next((s for s in students_list if s["student_id"] == student_id), None)

    if request.method == 'POST':
        student["name"] = request.form.get('name')
        student["email"] = request.form.get('email')
        student["department"] = request.form.get('department')
        student["year"] = request.form.get('year')
        student["gender"] = request.form.get('gender')
        student["address"] = request.form.get('address')
        student["room"] = request.form.get('room')
        student["contact"] = request.form.get('contact')
        student["admission_date"] = request.form.get('admission_date')
        student["fees_amount"] = request.form.get('fees_amount')
        student["fees_status"] = request.form.get('fees_status')
        return redirect('/students')

    return render_template("edit_student.html", student=student)


# ================= ROOMS =================
@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'POST':
        rooms_list.append({
            "room_number": request.form.get('room_number'),
            "room_type": request.form.get('room_type'),
            "room_status": request.form.get('room_status')
        })
        return redirect('/rooms')

    return render_template("rooms.html", rooms=rooms_list)


# ================= FEES =================
@app.route('/fees', methods=['GET', 'POST'])
def fees():
    if request.method == 'POST':
        fees_list.append({
            "student_name": request.form.get('student_name'),
            "room_number": request.form.get('room_number'),
            "amount": request.form.get('amount'),
            "status": request.form.get('status')
        })
        return redirect('/fees')

    return render_template("fees.html", fees=fees_list)


# ================= REPORT =================
@app.route('/reports')
def reports():
    return render_template("reports.html",
                           students=students_list,
                           rooms=rooms_list,
                           fees=fees_list)


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)