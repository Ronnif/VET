from app import create_app, db
from app.models import User

def create_admin(username, email, password):
    existing = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing:
        print(f'El usuario o email ya existe: {existing.username} / {existing.email}')
        return
    admin = User(username=username, email=email, role='admin')
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f'Admin user {username} created successfully.')

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        username = input('Enter admin username: ')
        email = input('Enter admin email: ')
        password = input('Enter admin password: ')
        create_admin(username, email, password)