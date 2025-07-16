from app import db
from app.models import Pet, ClinicalHistory, User, Appointment, Service, Client
from datetime import datetime, timezone

# --------- Mascotas ---------
def create_pet(name, species, breed, age, client_id):
    # Crear mascota
    pet = Pet(name=name, species=species, breed=breed, age=age, client_id=client_id)
    db.session.add(pet)
    db.session.commit()
    return pet

# --------- Citas ---------
def create_appointment(client_id, pet_id, service_id, vet_id, date, time):
    # Crear cita
    appointment = Appointment(
        client_id=client_id,
        pet_id=pet_id,
        service_id=service_id,
        vet_id=vet_id,
        date=date,
        time=time
    )
    db.session.add(appointment)
    db.session.commit()
    return appointment

# --------- Pagos ---------
def register_payment(appointment_id, payment_method=None, payment_amount=None):
    # Registrar pago de una cita
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        appointment.paid = True
        if payment_method is not None:
            appointment.payment_method = payment_method
        if payment_amount is not None:
            appointment.payment_amount = payment_amount
        appointment.payment_date = datetime.now(timezone.utc)
        db.session.commit()
        return appointment
    return None

# --------- Historial clínico ---------
def add_clinical_observation(pet_id, observation, appointment_id=None, vet_id=None):
    # Agregar observación clínica a una mascota
    clinical_history = ClinicalHistory(
        pet_id=pet_id,
        observation=observation,
        appointment_id=appointment_id,
        vet_id=vet_id  # <-- Aquí
    )
    db.session.add(clinical_history)
    db.session.commit()
    return clinical_history

# --------- Usuarios ---------
def create_user(username, email, role, password):
    # Crear usuario (admin, veterinario, recepcionista, etc.)
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(user_id):
    # Eliminar usuario por ID
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def change_user_password(user_id, new_password):
    # Cambiar contraseña de usuario
    user = User.query.get(user_id)
    if user:
        user.set_password(new_password)
        db.session.commit()
        return user
    return None

# --------- Clientes (Dueños) ---------
def create_client(name, email, phone=None, address=None, dni=None, notes=None):
    client = Client(
        name=name,
        email=email,
        phone=phone,
        address=address,
        dni=dni,
        notes=notes
    )
    db.session.add(client)
    db.session.commit()
    return client

# --------- Servicios ---------
def create_service(name, description=None, price=None):
    service = Service(name=name, description=description, price=price)
    db.session.add(service)
    db.session.commit()
    return service

def update_service(service_id, name=None, description=None, price=None):
    service = Service.query.get(service_id)
    if service:
        if name is not None:
            service.name = name
        if description is not None:
            service.description = description
        if price is not None:
            service.price = price
        db.session.commit()
        return service
    return None

def delete_service(service_id):
    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()
        return True
    return False