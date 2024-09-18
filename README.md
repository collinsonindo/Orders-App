# Orders-App
This is a simple customer and order management service written in Python + Flask. The service has a database where data about customers and orders is uploaded using REST API.  When an order is uploaded, the customer receives an SMS alerting them.

## Libraries/Python Packages Used
- [Flask](http://flask.pocoo.org/).
- [Flask-SQLAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/) interacting with the database.
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) handles SQLAlchemy database migrations.
- [Flask-OpenID](https://pythonhosted.org/Flask-OpenID/) to add OpenID based authentication.
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)  adds support for quickly building REST APIs.
- [Requests](https://pypi.org/project/requests/) to send HTTP/1.1 requests.
- [Pytest](https://docs.pytest.org/en/stable/) to write small, readable tests.
- [pytest-cov](https://pypi.org/project/pytest-cov/) for measuring coverage.
- [Authlib](https://docs.authlib.org/en/latest/) for OpenID Connect.
- [AfricasTalking](https://developers.africastalking.com/) SMS gateway and sandbox for sending SMS alerts to customers

The version used for each library is listed on [requirements.txt](https://github.com/collinsonindo/Orders-App/blob/main/requirements.txt)

  ## Features
- Manage Customers: Add and retrieve customer details.
- Manage Orders: Place and retrieve orders for customers.
- SMS Notifications: Send SMS alerts to customers using Africa's Talking SMS gateway.
- Authentication: Supports login via OpenID Connect (Google).
- RESTful API: Expose endpoints for managing customers and orders.
- Unit Testing: Comprehensive test coverage with CI/CD integration using Github Actions.

## Prerequisites
- Python 3.8+
- Africa's Talking API credentials
- A Google Cloud Project for OpenID Connect (OAuth 2.0) credentials

## Setup Instructions
1. Clone the Repository

```bash
git clone https://github.com/collinsonindo/Orders-App.git
cd Orders-App
```

2. Install Dependencies
Install the required Python packages:
bash
`pip install -r requirements.txt`


3. Run the Application
Run the Orders App

The application will be available at http://127.0.0.1:5000.

### API Endpoints
### Customers
GET customers: Retrieve a list of all customers.
`http://127.0.0.1:5000/customers`
The GET API works after user authentication.

POST customers: Add a new customer.
`http://127.0.0.1:5000/customers`
Payload
```
{
  "name": "Customer Name",
  "code": "CUST123",
  "phone_number": "+254711234567"
}
```
Does not require user authentication.

### Orders
GET orders: Retrieve a list of all orders.
`http://127.0.0.1:5000/orders`
The GET API works after user authentication.

POST orders: Add a new order.
`http://127.0.0.1:5000/orders`
Payload
```
{
  "item": "Item Name",
  "amount": 100,
  "customer_id": 1
}
```
The POST API does not require user authentication.

### Database
The POST customer and POST order saves data to a SQLITE database.
The Database contains 2 tables: Order table and Customer table.
The `customer_id` sets a relationship between the customer table and orders table

### Authentication
The application uses OpenID Connect for authentication, allowing users to log in with their Google accounts. Set up the Google OAuth 2.0 credentials in the Google Cloud Platform and configure the GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables.

### Testing
Unit tests are provided to ensure the application works as expected. To run the tests, use:

bash
`pytest --cov=ordersapp`

### Continuous Integration and Deployment
This project uses GitHub Actions for CI/CD. The workflow is defined in .github/workflows/cicd.yml. It performs the following tasks:

- Install dependencies
- Run tests with coverage
- Analyze the code for errors
