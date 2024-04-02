import unittest
import requests
import json

class TestFlaskApp(unittest.TestCase):
    base_url = 'http://127.0.0.1:5000'

    def test_register_user(self):
        url = f'{self.base_url}/users'
        data = {
            'username': 'testuser',
            'password': 'Test1234',
            'email': 'test@example.com',
            'dob': '1990-01-01',
            'credit_card': '1234567890123456'
        }
        response = requests.post(url, json=data)
        if response.status_code == 409:
          self.skipTest("Username already exists, registration failed")
        else:
          self.assertEqual(response.status_code, 201)

    def test_process_payment(self):
        # Register a user before making payment
        self.test_register_user()

        url = f'{self.base_url}/payments'
        data = {
            'credit_card': '1234567890123456',
            'amount': '100'
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_users(self):
        url = f'{self.base_url}/users'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_users_with_credit_card(self):
        url = f'{self.base_url}/users?CreditCard=yes'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_users_without_credit_card(self):
        url = f'{self.base_url}/users?CreditCard=no'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_credit_card_length(self):
        url = f'{self.base_url}/payments'
        data = {
            'credit_card': '1234567890',
            'amount': '100'
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_amount_length(self):
        url = f'{self.base_url}/payments'
        data = {
            'credit_card': '1234567890123456',
            'amount': '1000'
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_filter_value(self):
        url = f'{self.base_url}/users?CreditCard=invalid'
        response = requests.get(url)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
