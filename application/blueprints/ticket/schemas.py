from application.extensions import ma
from application.models import Ticket

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        include_fk = True

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

# class UpdateTicketSchema(ma.schema):
#     add_mechanic_ids = fields.List(fields.Int(), required=True)
#     remove_mechanic_ids = fields.List(fields.Int(), required=True)
#     class Meta:
#         fields = ("add_mechanic_ids", "remove_mechanic_ids")
