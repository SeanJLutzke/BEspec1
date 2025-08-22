from application.extensions import ma
from application.models import Part

class PartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Part

part_schema = PartSchema()
parts_schema = PartSchema(many=True)