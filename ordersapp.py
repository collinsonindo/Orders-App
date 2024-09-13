from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"<Customer {self.name}>"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def __repr__(self):
        return f"<Order {self.item} for Customer {self.customer_id}>"


with app.app_context():
    db.create_all()

# API to handle Customers
class CustomerAPI(Resource):
    def get(self):
        customers = Customer.query.all()
        return jsonify(
            [
                {
                    'id': customer.id, 
                    'name': customer.name, 
                    'code': customer.code
                } 
                for customer in customers
            ]
        )

    def post(self):
        data = request.json
        new_customer = Customer(name=data['name'], code=data['code'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(
            {
                'message': 'Customer added successfully!', 
                'customer': {
                    'name': new_customer.name, 
                    'code': new_customer.code
                    }
            }
        )

# API to handle Orders
class OrderAPI(Resource):
    def get(self):
        orders = Order.query.all()
        return jsonify(
            [
                {
                    'id': order.id, 
                    'item': order.item, 
                    'amount': order.amount, 
                    'time': order.time, 
                    'customer_id': order.customer_id
                } 
                for order in orders
            ]
        )

    def post(self):
        data = request.json
        new_order = Order(item=data['item'], amount=data['amount'], customer_id=data['customer_id'])
        db.session.add(new_order)
        db.session.commit()
        return jsonify(
            {
                'message': 'Order added successfully!', 
                'order': {
                    'item': new_order.item, 
                    'amount': new_order.amount, 
                    'time': new_order.time
                    }
            }
        )


api.add_resource(CustomerAPI, '/customers')
api.add_resource(OrderAPI, '/orders')

if __name__ == '__main__':
    app.run(debug=True)
