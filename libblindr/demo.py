import libblindr as bl
import os

# use dev mode for fast proofs
os.environ["RISC0_DEV_MODE"] = "true"

# server generates keypair for client

server_sk, server_pk = bl.server_generate_keypair()

# client has constraint and message

constraint = """{
  "auth": [
    ["password", "hello123"],
    ["What is your mothers maiden name", "Duke"],
    ["What is your favorite ice cream flavor", "chocolate"]
  ],
  "withdrawal_limit" : 100
}"""

contraint_hash = bl.hash_spend_constraint(constraint)

# server generates a new session (public and secret/private values)

server_sv, server_pv = bl.server_generate_session()

# client creates a new blind signing request and computes zero knowledge proof of transaction validity with constraint

# try making the amount too high. the generation of the zk proof will fail
transaction = """{
  "sender": "1FWu4Z9NoBWnguurBCdXpmM2xuiog6kbdy",
  "receiver": "3C3nZhpVjjDGo7vGzBCTJkKfYzCGWGLWsq",
  "amount": 100
}"""

blinded_transaction, request = bl.client_new_blind_request(transaction, server_pv)
proof = bl.prove_message_fits_constraint(constraint, transaction, server_pv)

# server verifies the proof of transaction validity of constraint hash and then blindly signs the message

is_valid_proof = bl.verify_message_fits_constraint(proof, blinded_transaction, contraint_hash)
assert(is_valid_proof)

blinded_signature = bl.server_sign(server_sk, server_sv, blinded_transaction)

# client unblinds the signature and can authenticate it

signature = bl.client_unblind_signature(request, blinded_signature)

is_valid_signature = bl.client_verify_signature(server_pk, signature)
assert(is_valid_signature)
