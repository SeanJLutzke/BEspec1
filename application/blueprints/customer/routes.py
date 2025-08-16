from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Ticket, Customer, db
from flask import Blueprint
from . import customers_bp



#customers_bp = Blueprint('customers', __name__)

@customers_bp.route("/", methods=["POST"])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(customer_name=customer_data["customer_name"], customer_email=customer_data["customer_email"], customer_phone=customer_data["customer_phone"]) #rip VIN
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

@customers_bp.route("/", methods=["GET"])
def get_customers():
    query =  select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200

@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error":"Invalid Customer ID"}), 400
    
    return customer_schema.jsonify(customer), 200

@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Invalid Customer ID"}), 400
    
    try:
         customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer.customer_name = customer_data["customer_name"]
#was VIN
    customer.customer_email = customer_data["customer_email"]
    customer.customer_phone = customer_data["customer_phone"]
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Invalid Customer ID"}), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted Customer {customer_id}."}), 200
