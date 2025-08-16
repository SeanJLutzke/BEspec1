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

db = SQLAlchemy()
ma = Marshmallow()
