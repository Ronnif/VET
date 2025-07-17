from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import Pet, ClinicalHistory, User, Appointment, Service, Client
from app.controllers import (
    create_pet, create_appointment, register_payment,
    add_clinical_observation, create_user, delete_user, change_user_password,
    create_client
)
from app.utils import success_response, error_response

# Prefijo global /api para todas las rutas
bp = Blueprint('main', __name__, url_prefix='/api')

# Mascotas (Pets)
@bp.route('/pets', methods=['GET'])
@jwt_required()
def api_get_pets():
    client_id = request.args.get('client_id')
    if client_id:
        pets = Pet.query.filter_by(client_id=client_id).all()
    else:
        pets = Pet.query.all()
    return jsonify([pet.to_dict() for pet in pets])

@bp.route('/pets/<int:pet_id>', methods=['GET'])
@jwt_required()
def api_get_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return jsonify(pet.to_dict())

@bp.route('/pets', methods=['POST'])
@jwt_required()
def api_create_pet():
    data = request.json
    required_fields = ['name', 'species', 'breed', 'age', 'client_id']
    for field in required_fields:
        if field not in data or data[field] in [None, '']:
            return jsonify(error_response(f"El campo '{field}' es obligatorio")), 400
    pet = create_pet(
        name=data['name'],
        species=data['species'],
        breed=data['breed'],
        age=data['age'],
        client_id=data['client_id']
    )
    return jsonify(success_response(pet.to_dict(), "Mascota registrada exitosamente")), 201

@bp.route('/pets/<int:pet_id>', methods=['PUT'])
@jwt_required()
def api_update_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    data = request.json
    pet.name = data.get('name', pet.name)
    pet.species = data.get('species', pet.species)
    pet.breed = data.get('breed', pet.breed)
    pet.age = data.get('age', pet.age)
    db.session.commit()
    return jsonify(success_response(pet.to_dict(), "Mascota actualizada"))

@bp.route('/pets/<int:pet_id>', methods=['DELETE'])
@jwt_required()
def api_delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    return jsonify(success_response(message="Mascota eliminada"))

# Citas (Appointments)
@bp.route('/appointments', methods=['GET'])
@jwt_required()
def api_get_appointments():
    appointments = Appointment.query.all()
    return jsonify([appointment.to_dict() for appointment in appointments])

@bp.route('/appointments/<int:appointment_id>', methods=['GET'])
@jwt_required()
def api_get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify(appointment.to_dict())

@bp.route('/appointments', methods=['POST'])
@jwt_required()
def api_create_appointment():
    data = request.json
    required_fields = ['client_id', 'pet_id', 'vet_id', 'service_id', 'date', 'time']
    for field in required_fields:
        if not data.get(field):
            return jsonify(error_response(f"El campo '{field}' es obligatorio")), 400
    appointment = create_appointment(
        client_id=data['client_id'],
        pet_id=data['pet_id'],
        vet_id=data['vet_id'],
        service_id=data['service_id'],
        date=data['date'],
        time=data['time'],
        pickup_code=data.get('pickup_code'),
        drop_off=data.get('drop_off', False)  # <-- Agrega esto
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify(success_response(appointment.to_dict(), "Cita registrada exitosamente")), 201

@bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def api_update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.json
    if 'date' in data:
        try:
            appointment.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except Exception:
            return jsonify(error_response("Formato de fecha inválido (YYYY-MM-DD)")), 400
    if 'time' in data:
        try:
            appointment.time = datetime.strptime(data['time'], '%H:%M').time()
        except Exception:
            return jsonify(error_response("Formato de hora inválido (HH:MM)")), 400
    if 'status' in data:
        appointment.status = data['status'].lower()
    if 'drop_off' in data:
        appointment.drop_off = data['drop_off']
    if 'pickup_code' in data:
        appointment.pickup_code = data['pickup_code']
    if 'collected' in data:
        appointment.collected = data['collected']
    db.session.commit()
    return jsonify(success_response(appointment.to_dict(), "Cita actualizada"))

@bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def api_delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify(success_response(message="Cita eliminada"))

@bp.route('/appointments/vet/<int:vet_id>', methods=['GET'])
@jwt_required()
def api_get_appointments_by_vet(vet_id):
    appointments = Appointment.query.filter_by(vet_id=vet_id).all()
    return jsonify([a.to_dict() for a in appointments])

@bp.route('/appointments/vet/me', methods=['GET'])
@jwt_required()
def api_get_my_appointments():
    current_user_id = int(get_jwt_identity())
    appointments = Appointment.query.filter_by(vet_id=current_user_id).all()
    return jsonify([a.to_dict() for a in appointments])

# Servicios (Services)
@bp.route('/services', methods=['GET'])
@jwt_required()
def api_get_services():
    services = Service.query.order_by(Service.id.desc()).all()
    return jsonify([service.to_dict() for service in services])

@bp.route('/services/<int:service_id>', methods=['GET'])
@jwt_required()
def api_get_service(service_id):
    service = Service.query.get_or_404(service_id)
    return jsonify(service.to_dict())

@bp.route('/services', methods=['POST'])
@jwt_required()
def api_create_service():
    data = request.json
    if (
        not data.get('name') or
        data.get('price') is None or data.get('price') == '' or
        not data.get('attention_type')
    ):
        return jsonify(error_response("El nombre, el precio y el tipo de atención son obligatorios")), 400
    try:
        service = Service(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            attention_type=data['attention_type']
        )
        db.session.add(service)
        db.session.commit()
        return jsonify(success_response(service.to_dict(), "Servicio creado exitosamente")), 201
    except Exception as e:
        return jsonify(error_response(str(e))), 400

@bp.route('/services/<int:service_id>', methods=['PUT'])
@jwt_required()
def api_update_service(service_id):
    service = Service.query.get_or_404(service_id)
    data = request.json
    if 'name' in data and not data['name']:
        return jsonify(error_response("El nombre no puede estar vacío")), 400
    if 'price' in data and data['price'] is None:
        return jsonify(error_response("El precio no puede estar vacío")), 400
    service.name = data.get('name', service.name)
    service.description = data.get('description', service.description)
    service.price = data.get('price', service.price)
    db.session.commit()
    return jsonify(success_response(service.to_dict(), "Servicio actualizado"))

@bp.route('/services/<int:service_id>', methods=['DELETE'])
@jwt_required()
def api_delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    from app.models import Appointment
    if Appointment.query.filter_by(service_id=service_id).first():
        return jsonify({"message": "No se puede eliminar el servicio porque está asociado a citas existentes."}), 400
    db.session.delete(service)
    db.session.commit()
    return jsonify(success_response(message="Servicio eliminado"))

# Usuarios (Users)
@bp.route('/users', methods=['GET'])
@jwt_required()
def api_get_users():
    role = request.args.get('role')
    if role:
        users = User.query.filter_by(role=role).all()
    else:
        users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def api_get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@bp.route('/users', methods=['POST'])
@jwt_required()
def api_create_user():
    data = request.json
    required_fields = ['username', 'email', 'role', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify(error_response(f"El campo '{field}' es obligatorio")), 400
    user = create_user(
        username=data['username'],
        email=data['email'],
        role=data['role'],
        password=data['password']
    )
    return jsonify(success_response(user.to_dict(), "Usuario creado exitosamente")), 201

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def api_delete_user(user_id):
    delete_user(user_id)
    return jsonify(success_response(message="Usuario eliminado"))

@bp.route('/users/<int:user_id>/password', methods=['PUT'])
@jwt_required()
def api_change_password(user_id):
    data = request.json
    if not data.get('new_password'):
        return jsonify(error_response("La nueva contraseña es obligatoria")), 400
    user = change_user_password(user_id, data['new_password'])
    if user:
        return jsonify(success_response(message="Contraseña actualizada"))
    return jsonify(error_response("Usuario no encontrado")), 404

# Login
@bp.route('/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify(error_response("Usuario y contraseña son obligatorios")), 400
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return jsonify(success_response({
            "user": user.to_dict(),
            "token": access_token
        }, "Login exitoso"))
    return jsonify(error_response("Credenciales incorrectas")), 401

# Clientes (Clients)
@bp.route('/clients', methods=['POST'])
@jwt_required()
def api_create_client():
    data = request.json
    if not data.get('name'):
        return jsonify(error_response("El nombre es obligatorio")), 400
    try:
        client = create_client(
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            dni=data.get('dni'),
            notes=data.get('notes')
        )
        return jsonify(success_response(client.to_dict(), "Cliente registrado exitosamente")), 201
    except Exception as e:
        return jsonify(error_response(str(e))), 400

@bp.route('/clients', methods=['GET'])
@jwt_required()
def api_get_clients():
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients])

# Pagos (Payments)
@bp.route('/payments', methods=['POST'])
@jwt_required()
def api_register_payment():
    data = request.json
    if not data.get('appointment_id'):
        return jsonify(error_response("El ID de la cita es obligatorio")), 400
    try:
        appointment = register_payment(
            appointment_id=data['appointment_id'],
            payment_method=data.get('payment_method'),
            payment_amount=data.get('payment_amount')
        )
        if appointment:
            return jsonify(success_response(appointment.to_dict(), "Pago registrado")), 200
        return jsonify(error_response("Cita no encontrada")), 404
    except Exception as e:
        return jsonify(error_response(str(e))), 400

@bp.route('/payments', methods=['GET'])
@jwt_required()
def api_get_payments():
    appointments = Appointment.query.filter_by(paid=True).all()
    return jsonify([a.to_dict() for a in appointments])

# Historial clínico (Clinical History)
@bp.route('/clinical-history', methods=['POST'])
@jwt_required()
def api_add_clinical_observation():
    data = request.json
    if not data.get('pet_id') or not data.get('observation'):
        return jsonify(error_response("El ID de la mascota y la observación son obligatorios")), 400
    vet_id = int(get_jwt_identity())
    clinical_history = add_clinical_observation(
        pet_id=data['pet_id'],
        observation=data['observation'],
        appointment_id=data.get('appointment_id'),
        vet_id=vet_id 
    )
    return jsonify(success_response(clinical_history.to_dict(), "Observación clínica agregada")), 201

@bp.route('/clinical-history/<int:history_id>', methods=['PUT'])
@jwt_required()
def api_update_clinical_history(history_id):
    data = request.json
    history = ClinicalHistory.query.get_or_404(history_id)
    if 'observation' in data and not data['observation']:
        return jsonify(error_response("La observación no puede estar vacía")), 400
    history.observation = data.get('observation', history.observation)
    db.session.commit()
    return jsonify(success_response(history.to_dict(), "Historial clínico actualizado"))

@bp.route('/clinical-history', methods=['GET'])
@jwt_required()
def api_get_clinical_history():
    appointment_id = request.args.get('appointment_id')
    query = ClinicalHistory.query
    if appointment_id:
        query = query.filter_by(appointment_id=appointment_id)
    history = query.all()
    return jsonify([h.to_dict() for h in history])

# Manejo de errores API
@bp.app_errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify(error_response("Not found", 404)), 404
    return jsonify({"error": "Not found"}), 404

@bp.app_errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify(error_response("Internal server error", 500)), 500
    return jsonify({"error": "Internal server error"}), 500

# Reportes de la API
@bp.route('/reports/payments', methods=['GET'])
@jwt_required()
def api_report_payments():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = Appointment.query.filter_by(paid=True)
    if start_date:
        query = query.filter(Appointment.payment_date >= start_date)
    if end_date:
        query = query.filter(Appointment.payment_date <= end_date)
    payments = query.all()
    total = sum(a.payment_amount or 0 for a in payments)
    return jsonify({
        "total_pagado": total,
        "pagos": [a.to_dict() for a in payments]
    })

@bp.route('/reports/appointments', methods=['GET'])
@jwt_required()
def api_report_appointments():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = Appointment.query
    if start_date:
        query = query.filter(Appointment.date >= start_date)
    if end_date:
        query = query.filter(Appointment.date <= end_date)
    appointments = query.all()
    return jsonify([a.to_dict() for a in appointments])

@bp.route('/reports/clinical-history', methods=['GET'])
@jwt_required()
def api_report_clinical_history():
    pet_id = request.args.get('pet_id')
    query = ClinicalHistory.query
    if pet_id:
        query = query.filter_by(pet_id=pet_id)
    history = query.all()
    return jsonify([h.to_dict() for h in history])