from app import create_app
from application.models import db, Part
import unittest
from datetime import datetime


class TestPart(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.part = Part(part_name="test_part", part_price=100000)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.part)
            db.session.commit()
            self.part_id = self.part.id
        self.client = self.app.test_client()

    def test_create_part(self):
        part_payload = {
        "part_name": "space wheels",
        "part_price": 100000,
    }
        response = self.client.post('/parts', json=part_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['part_name'], "space wheels")

    def test_invalid_creation(self):
        part_payload = {
        "part_name": "space wheels",
    }
        response = self.client.post('/parts', json=part_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['part_price'], ['Missing data for required field.'])

    def test_update_part(self):
        update_payload = {
            "part_name": "space wheels",
            "part_price": 100000,
        }
        response = self.client.put(f'/parts/{self.part_id}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['part_name'], 'space wheels') 
        self.assertEqual(response.json['part_price'], 100000)

    def test_get_part(self):
        response = self.client.get(f'/parts/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["part_name"], "test_part")

    def test_get_all_parts(self):
        response = self.client.get('/parts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['part_name'], "test_part")

    def test_delete_part(self):
        response = self.client.delete(f'/parts/{self.part_id}')
        self.assertEqual(response.status_code, 200)
