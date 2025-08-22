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
#part 1^^^^^
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache


limiter = Limiter(key_func=get_remote_address)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
