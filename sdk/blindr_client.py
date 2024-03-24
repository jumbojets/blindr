import requests
from blindr_config import BlindrConfig
from libblindr import hash_spend_constraint, prove_message_fits_constraint, client_new_blind_request, client_verify_signature, client_unblind_signature


# def hash_spend_constraint(constraint):
#     return constraint

# def prove_message_fits_constraint(constraint, message):
#     return True

# def client_new_blind_request(message, public_value):
#     return message, "blind_request"

# def client_unblind_signature(blind_request, blinded_signature):
#     return "signature"

# def client_verify_signature(public_key, signature):
#     return True


class MyAPIClient:
    def __init__(self, config: BlindrConfig):
        self.config = config

    def create_keys(self, constraint):
        constraint_hash = hash_spend_constraint(constraint)
        print(constraint_hash)
        response = requests.post(f"{self.config.base_url}/generate-keypair", json={"constraint_hash": constraint_hash})
        response.raise_for_status()  # This will raise an exception for HTTP error responses
        public_key = response.json().get('public_key')
        return {"public_key": public_key, "constraint_hash": constraint_hash}

    def create_or_restart_session(self, constraint):
        keys = self.create_keys(constraint)
        public_key, constraint_hash = keys['public_key'], keys['constraint_hash']
        response = requests.post(f"{self.config.base_url}/create-sign-session", json={"constraint_hash": constraint_hash})
        response.raise_for_status()
        public_value = response.json().get('public_value')
        return {"public_value": public_value, "public_key": public_key, "constraint_hash": constraint_hash}

    def sign_message(self, message, public_value, public_key, constraint):
        # Assuming `prove_message_fits_constraint` does some processing and returns a proof object
        proof = prove_message_fits_constraint(constraint, message)
        constraint_hash = hash_spend_constraint(constraint)

        # Assuming `client_new_blind_request` returns a tuple (blinded_message, blind_request)
        blinded_message, blind_request = client_new_blind_request(message, public_value)
        
        # Send the blinded message to the server for signing
        response = requests.post(f"{self.config.base_url}/blind-sign", json={
            "blinded_message": blinded_message, 
            "constraint_hash": constraint_hash, 
            "proof": proof
        })
        response.raise_for_status()
        blinded_signature = response.json().get('blinded_signature')
        
        # Assuming `client_unblind_signature` unblinds the signature
        signature = client_unblind_signature(blind_request, blinded_signature)
        
        # Optionally verify the signature - assuming this returns True if successful
        if client_verify_signature(public_key, signature):
            # End the session
            requests.post(f"{self.config.base_url}/close-sign-session", json={"constraint_hash": constraint_hash})
            return signature
        else:
            raise Exception("Signature verification failed")
        
    def create_session_and_sign(self, message, constraint):
        current_session = self.create_or_restart_session(constraint)
        signature = self.sign_message(message, current_session['public_value'], current_session['public_key'], constraint)
        return signature
    
    def delete_key(self, constraint):
        constraint_hash = hash_spend_constraint(constraint)
        response = requests.delete(f"{self.config.base_url}/delete-key", json={"constraint_hash": constraint_hash})
        response.raise_for_status()
        return True
