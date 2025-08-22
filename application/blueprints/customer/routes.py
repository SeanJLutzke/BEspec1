from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Ticket, Customer, db
from flask import Blueprint
from . import customers_bp
#part 1^^^^^
from application.extensions import limiter, cache
from application.utils.util import encode_token, token_required
from application.blueprints.ticket.schemas import tickets_schema


#customers_bp = Blueprint('customers', __name__)

@customers_bp.route("/", methods=["POST"])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(customer_name=customer_data["customer_name"], 
                            customer_email=customer_data["customer_email"], 
                            customer_phone=customer_data["customer_phone"], 
                            customer_password=customer_data["customer_password"])
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201
#apply pagination to get all route
@customers_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_customers():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        query =  select(Customer)
        pagination = db.paginate(query, page=page, per_page=per_page)
        customers = pagination.items if hasattr(pagination, 'items') else list(pagination)
        return customers_schema.jsonify(customers), 200
    except:
        query =  select(Customer)
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers), 200

@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error":"Invalid Customer ID"}), 400
    
    return customer_schema.jsonify(customer), 200

@customers_bp.route("/", methods=["PUT"])
@token_required
def update_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    #(OLD)customer = db.session.get(Customer, customer_id)
    customer = db.session.execute(query).scalars().first()

    if not customer:
        return jsonify({"error": "Invalid Customer ID"}), 400
    
    try:
         customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer.customer_name = customer_data["customer_name"]
    customer.customer_email = customer_data["customer_email"]
    customer.customer_phone = customer_data["customer_phone"]
    customer.customer_password = customer_data["customer_password"] 
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route("/", methods=["DELETE"])
@token_required
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    #(OLD)customer = db.session.get(Customer, customer_id)
    customer = db.session.execute(query).scalars().first()

    if not customer:
        return jsonify({"error": "Invalid Customer ID"}), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted Customer {customer_id}."}), 200
#part 1^^^^
@customers_bp.route("/login", methods=['POST'])
@limiter.limit("5 per hour")
def login():
    try:
        credentials = request.json
        username = credentials["customer_email"]
        password = credentials["customer_password"]
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password.'}), 400
    
    query = select(Customer).where(Customer.customer_email == username)
    customer = db.session.execute(query).scalar_one_or_none()
    #check on this if route is malfunctioning
    if customer and customer.customer_password == password:
        auth_token = encode_token(customer.id)
        response = {
            "status": "success",
            "messages": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'messages': "Username or Password incorrect (or both. That seems like something you would do.) "}), 401


# Make a route that Gets all tickets for an authenticated customer
@customers_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_customer_tickets(customer_id):
    query = select(Ticket).where(Ticket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()

    if not tickets:
        return jsonify({"error": "No tickets are associated with customer {customer_id}."}), 400

    return jsonify(tickets_schema.dump(tickets)), 200