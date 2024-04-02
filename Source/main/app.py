from flask import Flask, request, jsonify
from datetime import datetime
import re

app = Flask(__name__)

# Dummy database to store registered users
registered_users = []

# Dummy database to store credit card numbers
credit_cards = []


# Registration service
@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()

    # Validating request body
    if not all(key in data for key in ['username', 'password', 'email', 'dob']):
        return jsonify({'error': 'Missing required fields'}), 400

    username = data['username']
    password = data['password']
    email = data['email']
    dob = data['dob']
    credit_card = data.get('credit_card')

    # Basic validations
    if not username.isalnum():
        return jsonify({'error': 'Username should be alphanumeric'}), 400

    if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
        return jsonify({'error': 'Password must be at least 8 characters long and contain at least one digit and one uppercase letter'}), 400

    try:
        datetime.strptime(dob, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format for Date of Birth. Should be in ISO 8601 format (YYYY-MM-DD)'}), 400
    
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return jsonify({'error': 'Invalid email format'}), 400

    if credit_card:
    	if not credit_card.isdigit() or  len(credit_card) != 16:
        	return jsonify({'error': 'Invalid credit card number. It should have 16 digits'}), 400

    # Check age
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    age = (datetime.now() - dob_date).days // 365
    if age < 18:
        return jsonify({'error': 'User must be 18 or older to register'}), 403

    # Check if username already exists
    if any(user['username'] == username for user in registered_users):
        return jsonify({'error': 'Username already exists'}), 409

    # All validations passed, register the user
    registered_users.append({'username': username, 'password': password, 'email': email, 'dob': dob, 'credit_card': credit_card})
    if credit_card:
        credit_cards.append(credit_card)

    return jsonify({'message': 'User registered successfully'}), 201


# Payment service
@app.route('/payments', methods=['POST'])
def process_payment():
    data = request.get_json()

    # Validating request body
    if not all(key in data for key in ['credit_card', 'amount']):
        return jsonify({'error': 'Missing required fields'}), 400

    credit_card = data['credit_card']
    amount = data['amount']

    # Basic validations
    if not credit_card.isdigit() or len(credit_card) != 16:
        return jsonify({'error': 'Invalid credit card number. It should have 16 digits'}), 400

    if not amount.isdigit() or len(amount) != 3:
        return jsonify({'error': 'Invalid amount. It should have 3 digits'}), 400

    # Check if credit card is registered
    if credit_card not in credit_cards:
        return jsonify({'error': 'Credit card not registered'}), 404

    # Payment successful
    return jsonify({'message': 'Payment successful'}), 201


# GET /users endpoint
@app.route('/users', methods=['GET'])
def get_users():
    credit_card_filter = request.args.get('CreditCard')

    if credit_card_filter is None:
        return jsonify(registered_users)

    if credit_card_filter.lower() == 'yes':
        users_with_credit_card = [user for user in registered_users if user['credit_card']]
        return jsonify(users_with_credit_card)
    elif credit_card_filter.lower() == 'no':
        users_without_credit_card = [user for user in registered_users if not user['credit_card']]
        return jsonify(users_without_credit_card)
    else:
        return jsonify({'error': 'Invalid filter value. Use "Yes" or "No"'}), 400


if __name__ == '__main__':
    app.run(debug=True)
