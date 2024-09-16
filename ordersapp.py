from flask import Flask, redirect, request, jsonify, session, url_for
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime
import os
import uuid
import africastalking

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

# Africa's Talking Configuration
africas_talking_username = 'sandbox'  
africas_talking_api_key = 'atsk_c81ae0dd7543bfddafede8633f0f25bce0a5fe99ae29b752d788e3b41be97a4319ccdf37' 
africas_talking = africastalking.initialize(africas_talking_username, africas_talking_api_key)
sms = africastalking.SMS

# Configure OAuth for OpenID Connect
oauth = OAuth(app)
oauth.register(
    name='google',  
    client_id='25272599121-3e61tonp2hjrqmpqegdbs0m9fq5gqqdb.apps.googleusercontent.com',  
    client_secret='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', 
    #access_token_url='https://accounts.google.com/o/oauth2/token',
    #authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',  
    client_kwargs={
        'scope': 'openid profile email',  
    },
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

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

# Function to send SMS using Africa's Talking
def send_sms(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        print(response)
    except Exception as e:
        print(f"Error sending SMS: {e}")


# Authentication and Authorization

# Login route for OpenID Connect
@app.route('/login')
def login():
    # Generate a random nonce
    nonce = uuid.uuid4().hex
    # Store the nonce in the session
    session['nonce'] = nonce
    # Include the nonce in the authorize redirect
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)


# Callback route for OIDC authorization
@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    # Retrieve the nonce from the session
    nonce = session.pop('nonce', None)
    if nonce is None:
        return "Error: Nonce not found in session."

    # Pass the nonce to parse_id_token to validate the ID token
    user_info = oauth.google.parse_id_token(token, nonce=nonce)
    session['user'] = user_info  # Store user info in session
    return redirect('/dashboard')


# Protected route to view user dashboard
@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return jsonify({
        'message': 'Welcome to your dashboard!',
        'user': user
    })


# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# Authentication Decorator
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper



# API to handle Customers
class CustomerAPI(Resource):
    @login_required
    def get(self):
        customers = Customer.query.all()
        return jsonify(
            [
                {
                    'id': customer.id, 
                    'name': customer.name, 
                    'code': customer.code,
                    'phone_number': customer.phone_number
                } 
                for customer in customers
            ]
        )

    #@login_required
    def post(self):
        data = request.json
        new_customer = Customer(
            name=data['name'], 
            code=data['code'],
            phone_number=data['phone_number'] )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(
            {
                'message': 'Customer added successfully!', 
                'customer': {
                    'name': new_customer.name, 
                    'code': new_customer.code,
                    'phone_number': new_customer.phone_number
                    }
            }
        )

# API to handle Orders
class OrderAPI(Resource):
    @login_required
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

    #@login_required
    def post(self):
        data = request.json
        new_order = Order(item=data['item'], amount=data['amount'], customer_id=data['customer_id'])
        db.session.add(new_order)
        db.session.commit()

        # Fetch the customer's phone number to send the SMS
        customer = Customer.query.get(new_order.customer_id)
        if customer:
            message = f"Dear {customer.name}, your order for {new_order.item} has been received."
            send_sms(customer.phone_number, message)


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
