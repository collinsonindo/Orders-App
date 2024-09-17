import unittest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ordersapp import app, db, Customer, Order

class AppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
        self.client = self.app.test_client()
        
        # Create the database tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Test adding a new customer
    def test_add_customer(self):
        response = self.client.post('/customers', json={
            'name': 'Test Customer',
            'code': 'CUST100',
            'phone_number': '+254716913475'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customer added successfully!', response.data)

    # Test adding an order for a customer
    def test_add_order(self):
        # add a customer
        self.client.post('/customers', json={
            'name': 'Test Customer',
            'code': 'CUST100',
            'phone_number': '+254716913475'
        })

        # Add an order for the customer
        response = self.client.post('/orders', json={
            'item': 'Test Item',
            'amount': 100,
            'customer_id': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Order added successfully!', response.data)

    # Test retrieving customers
    def test_get_customers(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, [200, 302])

    # Test retrieving orders
    def test_get_orders(self):
        response = self.client.get('/orders')
        self.assertEqual(response.status_code, [200, 302])

if __name__ == '__main__':
    unittest.main()
