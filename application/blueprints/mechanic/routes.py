from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Ticket, Mechanic, db
from . import mechanics_bp


#CRUD for mechanics
@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanic(mechanic_name=mechanic_data["mechanic_name"], mechanic_salary=mechanic_data["mechanic_salary"], mechanic_phone=mechanic_data["mechanic_phone"], mechanic_email=mechanic_data["mechanic_email"])
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics),200
    
@mechanics_bp.route("/<int:mechanic_id>", methods=["GET"])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Invalid Mechanic Id"}), 400
    
    return mechanic_schema.jsonify(mechanic), 200


# route to list all mechanics in descending order of most ticket associations
@mechanics_bp.route("/popular", methods=["GET"])
def popular_mechanics(): 
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    mechanics.sort(key=lambda mechanic: len(mechanic.tickets), reverse=True)

    return mechanics_schema.jsonify(mechanics), 200

@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Invalid Mechanic ID"}), 400
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    mechanic.mechanic_name = mechanic_data["mechanic_name"]
    mechanic.mechanic_salary = mechanic_data["mechanic_salary"]
    mechanic.mechanic_phone = mechanic_data["mechanic_phone"]
    mechanic.mechanic_email = mechanic_data["mechanic_email"]

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Invalid Mechanic ID"}), 200
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"{mechanic.mechanic_name} has been executed. His kids cried like a bunch of little girls. You should have seen it."}), 200
