
from app import app, db
from models import User, Employee
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    # create default admin if not exists
    if not User.query.filter_by(email='admin@ondo.local').first():
        admin = User(email='admin@ondo.local', password_hash=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
    # sample employees
    if not Employee.query.first():
        e1 = Employee(name='Taro Yamada', email='taro@example.com', role='Engineer')
        e2 = Employee(name='Hanako Sato', email='hanako@example.com', role='Technician')
        db.session.add_all([e1,e2])
    db.session.commit()
    print('Initialized database with default admin and sample employees.')
