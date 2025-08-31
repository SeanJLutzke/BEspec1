from flask_app import create_app
from application.models import db, Customer, Ticket
import unittest
from datetime import datetime, timedelta, timezone
from application.utils.util import encode_token


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(customer_name="test_user", customer_email="test@email.com", customer_phone="8376458432" , customer_password='test')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            self.customer_id = self.customer.id
        self.token = encode_token(self.customer_id)
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "customer_name": "John Doe",
            "customer_email": "jd@email.com",
           	"customer_phone": "1234567890",
            "customer_password": "123"
        }

        response = self.client.post('/customers', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['customer_name'], "John Doe")

    def test_invalid_creation(self):
        customer_payload = {
            "customer_name": "John Doe",
            "customer_phone": "123-456-7890",
            "customer_password": "123"       
        }

        response = self.client.post('/customers', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['customer_email'], ['Missing data for required field.'])

        
    def test_login_customer(self):
        credentials = {
            "customer_email": "test@email.com",
            "customer_password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertIn("auth_token", response.json)
        return response.json['auth_token']
        
    def test_invalid_login(self):
        credentials = {
            "customer_email": "bad_email@email.com",
            "customer_password": "bad_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['messages'], "Username or Password incorrect (or both. That seems like something you would do.)")

    def test_update_customer(self):
        update_payload = {
            "customer_name": "Peter",
            "customer_phone": "8754765947",
            "customer_email": "test@email.com",
            "customer_password": "PetersPassword"
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['customer_name'], 'Peter') 
        self.assertEqual(response.json['customer_email'], 'test@email.com')

    def test_get_customer(self):
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.get(f'/customers/{self.customer_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['customer_name'], "test_user")


    def test_get_all_customers(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['customer_name'], "test_user")


    def test_delete_customer(self):
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_get_my_tickets(self):
        ticket_payload = {
            "ticket_date" : datetime.utcnow().isoformat(),
            "customer_id": self.customer_id,
            "vin": "NCC1701",
            "service_desc": "phase coil realignment"
        }
        create_resp = self.client.post('/tickets', json=ticket_payload)
        self.assertEqual(create_resp.status_code, 201)

        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        resp = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(any(t.get('vin') == "NCC1701" for t in data))