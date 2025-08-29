from app import create_app
from application.models import db, Ticket, Customer, Mechanic
import unittest
from datetime import datetime, timedelta, timezone


class TestTicket(unittest.TestCase):
    def setUp(self): 
        self.app = create_app('TestingConfig')

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            customer = Customer(
                customer_name="Jean-Luc Picard",
                customer_email="imisstheseason1tights@enterprise_d.com",
                customer_phone="555-1701",
                customer_password="IFartInTheTurboLift"
                )
            db.session.add(customer)
            db.session.commit()
            self.customer_id = customer.id

            ticket = Ticket(
                ticket_date=datetime.fromisoformat("2372-05-15T14:30:00"),
                customer_id=self.customer_id,
                vin="NCC1701D",
                service_desc="Turbolift Cabin Filter Replacement"
            )
            db.session.add(ticket)
            db.session.commit()
            self.ticket_id = ticket.id

        self.client = self.app.test_client()

    def test_create_ticket(self):
        ticket_payload = {
            "ticket_date": "2372-05-15T14:30:00",
            "customer_id": self.customer_id,
            "vin": "NCC1701E",
            "service_desc": "Turbolift Cabin Filter Replacement"
        }

        response = self.client.post('/tickets', json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["ticket_date"], ticket_payload["ticket_date"])
        self.assertEqual(data["customer_id"], self.customer_id)
        self.assertEqual(data["vin"], ticket_payload["vin"])
        self.assertEqual(data["service_desc"], ticket_payload["service_desc"])

    def test_invalid_creation(self):
        ticket_payload = {
            "ticket_date": "2372-05-15T14:30:00",
            "vin": "NCC1701D",
            "service_desc": "Turbolift Cabin Filter Replacement"       
        }
        response = self.client.post('/tickets', json=ticket_payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("customer_id", data)


    def test_update_ticket(self):
        with self.app.app_context():
            mechanic = Mechanic(
                mechanic_name="Geordi La Forge",
                mechanic_email="imfakingthewholeblindthing@enterprise_d.com",
                mechanic_phone="556-1701",
                mechanic_salary="100000"
            )
            db.session.add(mechanic)
            db.session.commit()
            mechanic_id = mechanic.id

        response = self.client.put(
            f"/tickets/{self.ticket_id}", json={"mechanic_id": mechanic_id, "action": "add"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("has been added", response.get_json().get("message", ""))


    def test_invalid_update_ticket(self):
        update_payload = {"mechanic_id": 1701, "action": "add"}
        response = self.client.put(f"/tickets/{self.ticket_id}", json=update_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json().get("error"), "Invalid Mechanic ID")

    def test_get_ticket(self):
        response = self.client.get(f"/tickets/{self.ticket_id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["vin"], "NCC1701D")

    def test_get_all_tickets(self):
        response = self.client.get('/tickets')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["vin"], "NCC1701D")
