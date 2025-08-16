from __future__ import annotations
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship, Session, Mapped, mapped_column
from sqlalchemy import create_engine, DateTime, ForeignKey, Table, Column, select, String, Integer, Float
from marshmallow import ValidationError
from typing import List, Optional
from datetime import datetime, timezone
from .extensions import db, ma
import os



#create base model
class Base(DeclarativeBase):
    pass

#Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)

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
    customer_name: Mapped[str] = mapped_column(String(75))
    customer_phone: Mapped[str] = mapped_column(String(15), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    #password
    

#one-to-many customer to tickets
    tickets: Mapped[List["Ticket"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan")
    
#ticket model
class Ticket(Base):
    __tablename__ = "tickets"

    mechanics: Mapped[List["Mechanic"]] = relationship(
        secondary=service_ticket, back_populates="tickets"
    )
#columns
    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    vin: Mapped[str] = mapped_column(String(17), unique=True,  nullable=False)
    service_desc: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_accounts.id"))
    customer: Mapped["Customer"] = relationship(back_populates="tickets")
#mechanic table
class Mechanic(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    mechanic_name: Mapped[str] = mapped_column(String(75), nullable=False)
    mechanic_phone: Mapped[str] = mapped_column(String(15), nullable=False)
    mechanic_salary: Mapped[float] = mapped_column(Float, nullable=False)
    mechanic_email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    tickets: Mapped[List["Ticket"]] = relationship(
        secondary=service_ticket, back_populates="mechanics"
    )