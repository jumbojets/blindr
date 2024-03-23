from flask import Flask, request, jsonify
from decouple import config
from db_connection import setup_db_connection
from models import PermanentStorage, TemporaryStorage
from db_methods import store_permanent, store_temporary, delete_temporary, find_permanent, find_temporary


app = Flask(__name__)

setup_db_connection(app)
app.config['SECRET_KEY'] = config('SECRET_KEY')

# Placeholder for your storage solution


@app.route('/generate-keypair', methods=['POST'])
def generate_keypair():
    data = request.json
    constraint_hash = data.get('constraint_hash')
    # private_key, public_key = server_generate_keypair()
    private_key = 'private_key1'
    public_key = 'public_key1'

    if find_permanent(constraint_hash):
        return jsonify(error="Constraint hash already exists"), 400
    # Store keys in a way that suits your application's requirements
    store_permanent(constraint_hash, private_key, public_key)
    
    return jsonify(public_key=public_key)

@app.route('/create-sign-session', methods=['POST'])
def create_sign_session():
    data = request.json
    constraint_hash = data.get('constraint_hash')
    if find_permanent(constraint_hash) is None:
        return jsonify(error="Constraint hash not found"), 404
    
    temp_entry = find_temporary(constraint_hash)
    if temp_entry:
        print('found session alr exists')
        return jsonify(public_value=temp_entry.public_value)

    # private_value, public_value = server_generate_session()
    private_value = 'private_value1'
    public_value = 'public_value1'
    # Store session data with constraint_hash as a key or another identifier
    store_temporary(constraint_hash, private_value, public_value)
    return jsonify(public_value=public_value)

@app.route('/close-sign-session', methods=['POST'])
def close_sign_session():
    data = request.json
    constraint_hash = data.get('constraint_hash')
    # Remove session data associated with the constraint_hash
    delete_temporary(constraint_hash)
    return jsonify(success=True)

@app.route('/blind-sign', methods=['POST'])
def blind_sign():
    data = request.json
    blinded_message = data.get('blinded_message')
    constraint_hash = data.get('constraint_hash')
    proof = data.get('proof')

    if find_temporary(constraint_hash) is None:
        return jsonify(error="Session not found"), 404
    
    permanent_entry = find_permanent(constraint_hash)
    if permanent_entry is None:
        return jsonify(error="Constraint hash not found"), 404
    
    # Verify the message fits the constraint
    # is_valid = verify_message_fits_constraint(blinded_message, constraint_hash, proof)
    # if not is_valid:
    #     return jsonify(error="Verification failed"), 400
    # private_key = permanent_entry.private_key
    # blinded_signature = server_sign(private_key, blinded_message) 
    blinded_signature = "signed" 
    return jsonify(blinded_signature=blinded_signature)

if __name__ == '__main__':
    app.run(debug=True)
