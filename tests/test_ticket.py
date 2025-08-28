from app import create_app
from application.models import db, Ticket
import unittest
from datetime import datetime

#new_ticket = Ticket(ticket_date=ticket_data["ticket_date"], customer_id=ticket_data["customer_id"], vin=ticket_data["vin"], service_desc=ticket_data["service_desc"]

class TestTicket(unittest.TestCase):
    def setUp(self): 
        self.app = create_app('TestingConfig')
        self.ticket = Ticket(ticket_date="test_user", customer_id=1, vin="8376458432" , service_desc='100000')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.ticket)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_ticket(self):
        ticket_payload = {
        "ticket_date": "2372-05-15T14:30:00",
        "customer_id": 1,
        "vin": "^",
        "service_desc": "123"
    }

        response = self.client.post('/tickets', json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['ticket_date'], "2372-05-15T14:30:00")

        def test_invalid_creation(self):
            ticket_payload = {
            "ticket_date": "2372-05-15T14:30:00",
            "vin": "^",
            "service_desc": "123"       
        }

        response = self.client.post('/tickets', json=ticket_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['customer_id'], ['Missing data for required field.'])

    def test_update_ticket(self):
        update_payload = {
            "ticket_date": "2372-05-15T14:30:00",
            "vin": "^",
            "customer_id": 1,
            "service_desc": "10000000"
        }

        response = self.client.put('/tickets/<int: ticket_id>', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['ticket_date'], "2372-05-15T14:30:00") 
        self.assertEqual(response.json['customer_id'], 'test@email.com')

#DONT FORGET TO ADD GET 1

    def test_get_all_tickets(self):
        response = self.client.get('/tickets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['ticket_date'], "test_user")

