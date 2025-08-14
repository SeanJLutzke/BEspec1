from __future__ import annotations
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship, Session, Mapped, mapped_column
from sqlalchemy import create_engine, DateTime, ForeignKey, Table, Column, select, String, Integer, Float
from marshmallow import ValidationError
from typing import List, Optional
from datetime import datetime, timezone
import os

#Initialization
app = Flask(__name__)

#config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rootuser@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create base model
class Base(DeclarativeBase):
    pass

#Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

#service-ticket association table
service_ticket = Table(
    "service_tickets",
    Base.metadata,
    Column("ticket_id", Integer, ForeignKey("tickets.id"), primary_key=True),
    Column("mechanic_id", Integer, ForeignKey("mechanics.id"), primary_key=True),
)
#Class Definitions
class Customer(Base):
    __tablename__ = "customer_accounts"

#columns (auto-inc is redundant/ on by default for primary keys)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(75))
    vin: Mapped[str] = mapped_column(String(17), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    #password
    

#one-to-many customer to tickets
    tickets: Mapped[List["Ticket"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan")
    
#ticket model
class Ticket(Base):
    __tablename__ = "tickets"

    mechanics: Mapped[List["Mechanic"]] = relationship(
        secondary=ticket_mechanic, back_populates="tickets"
    )
#columns
    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_accounts.id"))
    customer: Mapped["Customer"] = relationship(back_populates="tickets")
#mechanic table
class Mechanic(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    mechanic_name: Mapped[str] = mapped_column(String(75), nullable=False)
    hourly_rate: Mapped[float] = mapped_column(Float, nullable=False)
    tickets: Mapped[List["Ticket"]] = relationship(
        secondary=ticket_mechanic, back_populates="mechanics"
    )

#Schemas Schemas Schemas Schemas Schemas Schemas Schemas Schemas 
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        include_fk = True

#Initialize Schemas
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

#CRUD 

#CRUD for customers
@app.route("/customers", methods=["POST"])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(name=customer_data["name"], vin=customer_data["vin"], email=customer_data["email"])
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

@app.route("/customers", methods=["GET"])
def get_customers():
    query =  select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200

@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error":"Invalid Customer ID"}), 400
    
    return customer_schema.jsonify(customer), 200

@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Invalid Customer ID"}), 400
    
    try:
         customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer.name = customer_data["name"]
    customer.vin = customer_data["vin"]
    customer.email = customer_data["email"]
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Invalid Customer ID"}), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted Customer {customer_id}."}), 200

#CRUD for tickets
@app.route("/tickets", methods=["POST"])
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = Ticket(ticket_date=ticket_data["ticket_date"], customer_id=ticket_data["customer_id"])
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

@app.route("/tickets", methods=["GET"])
def get_tickets():
    query = select(Ticket)
    tickets = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(tickets), 200

@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return jsonify({"error": "Invalid Ticket ID"}), 400
    
    return ticket_schema.jsonify(ticket), 200

@app.route("/tickets/<int:ticket_id>", methods=["PUT"])
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
    
@app.route("/tickets/<int:ticket_id>", methods=["Delete"])
def delete_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return jsonify({"error": "Invalid ticket ID"}), 400
    
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"{ticket_id} has been deleted."}), 200

#CRUD for mechanics
@app.route("/mechanics", methods=["POST"])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanic(mechanic_name=mechanic_data["mechanic_name"], hourly_rate=mechanic_data["hourly_rate"])
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@app.route("/mechanics", methods=["GET"])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics),200
    
@app.route("/mechanics/<int:mechanic_id>", methods=["GET"])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Invalid Mechanic Id"}), 400
    
    return mechanic_schema.jsonify(mechanic), 200

@app.route("/mechanics/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Invalid Mechanic ID"}), 400
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    mechanic.mechanic_name = mechanic_data["mechanic_name"]
    mechanic.hourly_rate = mechanic_data["hourly_rate"]
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@app.route("/mechanics/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Invalid Mechanic ID"}), 200
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"{mechanic.mechanic_name} has been executed. His kids cried like a bunch of little girls. You should have seen it."}), 200

# "load-bearing coconut"
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# WINDOWS KEY + R
# search "services.msc"
# find MySQL84
# right click it 
# open MySQL


    



                        
