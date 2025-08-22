from .schemas import part_schema, parts_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Part, Ticket, db
from flask import Blueprint
from . import parts_bp
from application.blueprints.ticket.schemas import tickets_schema

@parts_bp.route("/", methods=["POST"])
def create_part():
    try:
        part_data = part_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_part = Part(part_name=part_data["part_name"], part_price=part_data["part_price"])
    db.session.add(new_part)
    db.session.commit()

    return part_schema.jsonify(new_part), 201

@parts_bp.route("/", methods=["GET"])
def get_parts():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 25))
        query = select(Part)
        parts = db.paginate(query, page=page, per_page=per_page)
        return jsonify(parts_schema.dump(parts.items)), 200
    except:
        query = select(Part)
        parts = db.session.execute(query).scalars().all()
        return parts_schema.jsonify(parts), 200
    
@parts_bp.route("/<int:part_id>", methods=["GET"])
def get_part(part_id):
    part = db.session.get(Part, part_id)

    if not part:
        return jsonify({"error": "Invalid Part ID"}), 400
    
    return part_schema.jsonify(part), 200

@parts_bp.route("/<int:part_id>", methods=["PUT"])
def update_part(part_id):
    part = db.session.get(Part, part_id)

    if not part:
        return jsonify({"error": "Invalid Part ID"}), 400
    try:
        part_data = part_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    part.part_name = part_data["part_name"]
    part.part_price = part_data["part_price"]

    db.session.commit()
    return part_schema.jsonify(part), 200

@parts_bp.route("/<int:part_id>", methods=["DELETE"])
def delete_part(part_id):
    part = db.session.get(Part, part_id)

    if not part:
        return jsonify({"error": "Invalid Part ID"}), 400
    
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": "Part deleted successfully."}), 200