# from app import create_app
# from application.models import db, Mechanic
# import unittest
# from datetime import datetime


# class TestMechanic(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('TestingConfig')
#         self.mechanic = Mechanic(mechanic_name="test_user", mechanic_email="test@email.com", mechanic_phone="8376458432" , mechanic_salary='100000')
#         with self.app.app_context():
#             db.drop_all()
#             db.create_all()
#             db.session.add(self.mechanic)
#             db.session.commit()
#         self.client = self.app.test_client()

#     def test_create_mechanic(self):
#         mechanic_payload = {
#         "mechanic_name": "John Doe",
#         "mechanic_email": "jd@email.com",
#         "mechanic_phone": "1234567890",
#         "mechanic_salary": "123"
#     }

#         response = self.client.post('/mechanics', json=mechanic_payload)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json['mechanic_name'], "John Doe")

#         def test_invalid_creation(self):
#             mechanic_payload = {
#             "mechanic_name": "John Doe",
#             "mechanic_phone": "123-456-7890",
#             "mechanic_salary": "123"       
#         }

#         response = self.client.post('/mechanics', json=mechanic_payload)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json['mechanic_email'], ['Missing data for required field.'])

#     def test_update_mechanic(self):
#         update_payload = {
#             "mechanic_name": "Peter",
#             "mechanic_phone": "8754765947",
#             "mechanic_email": "test@email.com",
#             "mechanic_salary": "10000000"
#         }

#         response = self.client.put('/mechanics/<int: mechanic_id>', json=update_payload)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json['mechanic_name'], 'Peter') 
#         self.assertEqual(response.json['mechanic_email'], 'test@email.com')


# #DONT FORGET TO ADD GET 1


#     def test_get_all_mechanics(self):
#         response = self.client.get('/mechanics')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json[0]['mechanic_name'], "test_user")


#     def test_delete_mechanic(self):
#         response = self.client.delete('/mechanics/<int: mechanic_id>')
#         self.assertEqual(response.status_code, 200)
