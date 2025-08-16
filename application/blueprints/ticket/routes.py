from .schemas import ticket_schema, tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Ticket, Mechanic, db
from . import tickets_bp


@tickets_bp.route("/", methods=["POST"])
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = Ticket(ticket_date=ticket_data["ticket_date"], customer_id=ticket_data["customer_id"], vin=ticket_data["vin"], service_desc=ticket_data["service_desc"])
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

@tickets_bp.route("/", methods=["GET"])
def get_tickets():
    query = select(Ticket)
    tickets = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(tickets), 200

@tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return jsonify({"error": "Invalid Ticket ID"}), 400
    
    return ticket_schema.jsonify(ticket), 200

@tickets_bp.route("/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return jsonify({"error": "Invalid Ticket ID"}), 400
    
    mechanic_id = request.json.get("mechanic_id")
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Invalid Mechanic ID"}), 400
    
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
        return jsonify({"message": f"Ticket {ticket_id} has been updated."}), 200
    else:
        return jsonify({"message": f"Mechanic is already on ticket {ticket_id}."}), 200
    
@tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return jsonify({"error": "Invalid ticket ID"}), 400
    
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"{ticket_id} has been deleted."}), 200
