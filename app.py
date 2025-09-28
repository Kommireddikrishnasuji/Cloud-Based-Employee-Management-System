
from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Employee, Attendance, LeaveRequest
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_this_in_production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    total_employees = Employee.query.count()
    total_attendance = Attendance.query.count()
    leave_pending = LeaveRequest.query.filter_by(status='Pending').count()
    # simple stats for chart
    from sqlalchemy import func
    hires_by_month = (
        db.session.query(func.strftime('%Y-%m', Employee.hired_on), func.count(Employee.id))
        .group_by(func.strftime('%Y-%m', Employee.hired_on)).all()
    )
    labels = [r[0] for r in hires_by_month]
    values = [r[1] for r in hires_by_month]
    return render_template('dashboard.html', total_employees=total_employees,
                           total_attendance=total_attendance, leave_pending=leave_pending,
                           chart_labels=labels, chart_values=values)

@app.route('/employees')
@login_required
def employees():
    emps = Employee.query.all()
    return render_template('employees.html', employees=emps)

@app.route('/employee/add', methods=['GET','POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        hired_on = request.form.get('hired_on') or datetime.utcnow().date().isoformat()
        emp = Employee(name=name, email=email, role=role, hired_on=hired_on)
        db.session.add(emp)
        db.session.commit()
        flash('Employee added', 'success')
        return redirect(url_for('employees'))
    return render_template('add_employee.html')

@app.route('/employee/<int:emp_id>/edit', methods=['GET','POST'])
@login_required
def edit_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    if request.method == 'POST':
        emp.name = request.form['name']
        emp.email = request.form['email']
        emp.role = request.form['role']
        db.session.commit()
        flash('Updated', 'success')
        return redirect(url_for('employees'))
    return render_template('edit_employee.html', emp=emp)

@app.route('/employee/<int:emp_id>/delete', methods=['POST'])
@login_required
def delete_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    db.session.delete(emp)
    db.session.commit()
    flash('Deleted', 'success')
    return redirect(url_for('employees'))

@app.route('/attendance/mark/<int:emp_id>', methods=['POST'])
@login_required
def mark_attendance(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    att = Attendance(employee_id=emp.id, timestamp=datetime.utcnow())
    db.session.add(att)
    db.session.commit()
    return jsonify({'status':'ok'})

@app.route('/leaves', methods=['GET','POST'])
@login_required
def leaves():
    if request.method == 'POST':
        emp_id = int(request.form['employee_id'])
        reason = request.form['reason']
        lr = LeaveRequest(employee_id=emp_id, reason=reason, status='Pending')
        db.session.add(lr)
        db.session.commit()
        flash('Leave requested', 'success')
        return redirect(url_for('leaves'))
    all_leaves = LeaveRequest.query.order_by(LeaveRequest.created_on.desc()).all()
    emps = Employee.query.all()
    return render_template('leaves.html', leaves=all_leaves, employees=emps)

@app.route('/leave/<int:leave_id>/action', methods=['POST'])
@login_required
def leave_action(leave_id):
    lr = LeaveRequest.query.get_or_404(leave_id)
    action = request.form['action']
    if action in ['Approve','Reject']:
        lr.status = 'Approved' if action=='Approve' else 'Rejected'
        db.session.commit()
    return redirect(url_for('leaves'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
