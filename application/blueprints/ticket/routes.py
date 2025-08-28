from .schemas import ticket_schema, tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Ticket, Mechanic, db
from . import tickets_bp


@tickets_bp.route("/", methods=["POST"], strict_slashes=False)
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = Ticket(ticket_date=ticket_data["ticket_date"], customer_id=ticket_data["customer_id"], vin=ticket_data["vin"], service_desc=ticket_data["service_desc"])
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

@tickets_bp.route("/", methods=["GET"], strict_slashes=False)
def get_tickets():
    query = select(Ticket)
    tickets = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(tickets), 200

@tickets_bp.route("/<int:ticket_id>", methods=["GET"], strict_slashes=False)
def get_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return jsonify({"error": "Invalid Ticket ID"}), 400
    
    return ticket_schema.jsonify(ticket), 200

@tickets_bp.route("/<int:ticket_id>", methods=["PUT"], strict_slashes=False)
def update_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return jsonify({"error": "Invalid Ticket ID"}), 400
    
    mechanic_id = request.json.get("mechanic_id")
    action = request.json.get("action", "add")
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Invalid Mechanic ID"}), 400
    #add by { "mechanic_id" : 1, "action": "add"}
    #remove by { "mechanic_id" : 1, "action": "remove"}
    
    if action == "remove":
        if mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
            db.session.commit()
            return jsonify({"message": f"Mechanic {mechanic_id} has been removed from ticket {ticket_id}."}), 200
        else:
            return jsonify({"message": f"Mechanic {mechanic_id} already wasn't on ticket {ticket_id}, but we'll let him know you don't like him."}), 200
    else:
        if mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
            db.session.commit()
            return jsonify({"message": f"Ticket {ticket_id} has been updated. Mechanic {mechanic_id} has been added."}), 200
        else:
            return jsonify({"message": f"Mechanic is already on ticket {ticket_id}."}), 200
        

    

#Being able to delete tickets can make testing easier, but shouldn't be an option in deployment
#Also it makes more work when counting the tickets a mechanic has worked on because then you have to store that

# @tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
# def delete_ticket(ticket_id):
#     ticket = db.session.get(Ticket, ticket_id)

#     if not ticket:
#         return jsonify({"error": "Invalid ticket ID"}), 400
    
#     db.session.delete(ticket)
#     db.session.commit()
#     return jsonify({"message": f"{ticket_id} has been deleted."}), 200
