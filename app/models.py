from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone 


# Modelo de Usuario
class User(db.Model):
    """
    Representa a un usuario del sistema (admin, veterinario, recepcionista o cliente).
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False)  # admin, vet, recepcionista, client

    def set_password(self, password):
        # Guarda la contraseña de forma segura (hash)
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Verifica la contraseña
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        # Serializa el usuario a un diccionario (para respuestas JSON)
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }

# Modelo de Mascota
class Pet(db.Model):
    """
    Representa una mascota registrada en el sistema.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    client = db.relationship('Client', backref=db.backref('pets', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "client_id": self.client_id,
            "client": self.client.to_dict() if self.client else None
        }

# Modelo de Cita
class Appointment(db.Model):
    """
    Representa una cita veterinaria entre un cliente, su mascota y un veterinario.
    """
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    time = db.Column(db.Time, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(50))
    payment_amount = db.Column(db.Float)
    payment_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Pendiente')  
    drop_off = db.Column(db.Boolean, default=False)
    pickup_code = db.Column(db.String(20))
    collected = db.Column(db.Boolean, default=False)

    client = db.relationship('Client', foreign_keys=[client_id]) 
    pet = db.relationship('Pet', backref=db.backref('appointments', lazy=True))
    vet = db.relationship('User')
    service = db.relationship('Service', backref=db.backref('appointments', lazy=True))

    def to_dict(self):
        # Serializa la cita a un diccionario (incluye datos relacionados)
        return {
            "id": self.id,
            "client_id": self.client_id,
            "pet_id": self.pet_id,
            "vet_id": self.vet_id,
            "service_id": self.service_id,
            "date": self.date.isoformat() if self.date else None,
            "time": self.time.isoformat() if self.time else None,
            "paid": self.paid,
            "payment_method": self.payment_method,
            "payment_amount": self.payment_amount,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "client": self.client.to_dict() if self.client else None,
            "pet": self.pet.to_dict() if self.pet else None,
            "vet": self.vet.to_dict() if self.vet else None,
            "service": self.service.to_dict() if self.service else None,
            "status": self.status,
            "drop_off": self.drop_off,
            "pickup_code": self.pickup_code,
            "collected": self.collected,
        }
# Modelo de Servicio
class Service(db.Model):
    """
    Representa un servicio veterinario ofrecido (consulta, cirugía, etc.).
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    attention_type = db.Column(db.String(80), nullable=False)  # Ej: presencial, a domicilio

    def to_dict(self):
        # Serializa el servicio a un diccionario
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "attention_type": self.attention_type
        }

# Modelo de Historial Clínico
class ClinicalHistory(db.Model):
    """
    Representa una observación clínica registrada para una mascota.
    """
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    observation = db.Column(db.Text, nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=True)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    vet_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    vet = db.relationship('User')

    pet = db.relationship('Pet', backref=db.backref('clinical_histories', lazy=True))
    appointment = db.relationship('Appointment', backref=db.backref('clinical_histories', lazy=True))

    def to_dict(self):
        # Serializa el historial clínico a un diccionario (incluye datos relacionados)
        return {
            "id": self.id,
            "pet_id": self.pet_id,
            "observation": self.observation,
            "appointment_id": self.appointment_id,
            "date": self.date.isoformat(),
            "vet_id": self.vet_id,
            "pet": self.pet.to_dict() if self.pet else None,
            "appointment": self.appointment.to_dict() if self.appointment else None,
            "veterinarian_name": self.vet.username if self.vet else None,
            "owner_name": self.pet.client.name if self.pet and self.pet.client else None,
            "service_name": self.appointment.service.name if self.appointment and self.appointment.service else None
        }

# Modelo de Cliente
class Client(db.Model):
    """
    Representa un cliente del sistema (dueño de la mascota).
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    dni = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    notes = db.Column(db.Text)     

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "dni": self.dni,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "notes": self.notes
        }