import requests

# Base URL of the Flask application
base_url = 'http://127.0.0.1:5000'

# Function to register a user
def register_user(username, password, email, dob, credit_card=None):
    url = f'{base_url}/users'
    data = {
        "username": username,
        "password": password,
        "email": email,
        "dob": dob,
        "credit_card": credit_card
    }
    response = requests.post(url, json=data)
    return response.json()

# Function to make a payment
def make_payment(credit_card, amount):
    url = f'{base_url}/payments'
    data = {
        "credit_card": credit_card,
        "amount": amount
    }
    response = requests.post(url, json=data)
    return response.json()

if __name__ == '__main__':
    # Register a user
    register_response = register_user('ann', 'Ann23ew1', 'ann@example.com', '2005-01-03', '9876543210123456')
    print(register_response)

    # Make a payment
    payment_response = make_payment('9876543210123456', '900')
    print(payment_response)
