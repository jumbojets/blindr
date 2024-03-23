use pyo3::prelude::*;
use blindsign::{session::BlindSession, keypair::BlindKeypair, request::BlindRequest, signature::WiredUnblindedSigData};
use blindr_common::{Transaction, Constraint, Auth};
use std::convert::TryInto;
use curve25519_dalek::{scalar::Scalar, ristretto::CompressedRistretto};
use base64::prelude::*;

#[pyfunction]
fn server_generate_keypair() -> PyResult<(String, String)> {
    let keypair = BlindKeypair::generate().unwrap();
    let private_key = keypair.private().to_bytes();
    let public_key = keypair.public().compress().to_bytes();
    let private_key_hex = hex::encode(private_key);
    let public_key_hex = hex::encode(public_key);
    Ok((private_key_hex, public_key_hex))
}

#[pyfunction]
fn server_generate_session() -> PyResult<(String, String)> {
    let (public_value_bytes, private_value) = BlindSession::new().unwrap();
    let private_value_bytes = private_value.k.to_bytes();
    let private_value_hex = hex::encode(private_value_bytes);
    let public_value_bytes = hex::encode(public_value_bytes);
    Ok((private_value_hex, public_value_bytes))
}

#[pyclass]
pub struct PyBlindRequest(BlindRequest);

#[pyfunction]
fn client_new_blind_request(transaction: String, public_value_hex: String) -> PyResult<(String, PyBlindRequest)> {
    let message = Transaction::from_str(&transaction).message();
    let public_value = hex::decode(public_value_hex).unwrap().try_into().unwrap();
    
    // return blinded_message and blind_request
    let (blinded_message, blind_request) = BlindRequest::new_specific_msg(&public_value, &message).unwrap();
    let blinded_message_hex = hex::encode(blinded_message);
    let blind_request_py = PyBlindRequest(blind_request);
    Ok((blinded_message_hex, blind_request_py))
}

#[pyfunction]
fn server_sign(private_key_hex: String, private_value_hex: String, blinded_message_hex: String) -> PyResult<String> {
    let private_key_bytes = hex::decode(private_key_hex).unwrap().try_into().unwrap();
    let private_key_scalar = Scalar::from_bits(private_key_bytes);

    let private_value_bytes = hex::decode(private_value_hex).unwrap().try_into().unwrap();
    let private_value_scalar = Scalar::from_bits(private_value_bytes);
    let private_value = BlindSession { k: private_value_scalar };

    let blinded_message_bytes: [u8; 32] = hex::decode(blinded_message_hex).unwrap().try_into().unwrap();

    // return blinded signature
    let blinded_signature = private_value.sign_ep(&blinded_message_bytes, private_key_scalar).unwrap();
    let blinded_signature_hex = hex::encode(blinded_signature);
    Ok(blinded_signature_hex)
}

#[pyfunction]
fn client_unblind_signature(blind_request: PyRef<PyBlindRequest>, blinded_signature_hex: String) -> PyResult<String> {
    let blinded_signature_bytes = hex::decode(blinded_signature_hex).unwrap().try_into().unwrap();

    let unblinded_sig_msg = blind_request.0.gen_signed_msg(&blinded_signature_bytes).unwrap();
    let unblinded_sig_bytes = WiredUnblindedSigData::from(unblinded_sig_msg).to_bytes();
    let unblinded_sig_hex = hex::encode(unblinded_sig_bytes);

    Ok(unblinded_sig_hex)
}

#[pyfunction]
fn client_verify_signature(public_key_hex: String, signature_hex: String) -> PyResult<bool> {
    let public_key_bytes = hex::decode(public_key_hex).unwrap().try_into().unwrap();
    let public_key = CompressedRistretto(public_key_bytes).decompress().unwrap();

    let signature_bytes = hex::decode(signature_hex).unwrap().try_into().unwrap();
    let sig = WiredUnblindedSigData(signature_bytes).to_internal_format().unwrap();

    let isok = sig.authenticate(public_key);
    Ok(isok)
}


#[pyfunction]
fn hash_spend_constraint(constraint: String) -> PyResult<String> {
    let digest = Constraint::from_str(&constraint).hash();
    let digest_hex = hex::encode(digest);
    Ok(digest_hex)
}

#[pyfunction]
fn prove_message_fits_constraint(auth: String, constraint: String, transaction: String) -> PyResult<String> {
    let auth = Auth::from_str(&auth);
    let constraint = Constraint::from_str(&constraint);
    let transaction = Transaction::from_str(&transaction);
    let (receipt, _, _) = blindr_zk_driver::prove(&transaction, &auth, &constraint);
    let receipt_bin = bincode::serialize(&receipt).unwrap();
    let receipt_base64 = BASE64_STANDARD.encode(receipt_bin);
    Ok(receipt_base64)
    
}

#[pyfunction]
fn verify_message_fits_constraint(receipt_base64: String, _blinded_message: String, _constraint_hash: String) -> PyResult<bool> {
    // TODO: we need to check _blinded_message and _constraint_hash
    let receipt_bin = BASE64_STANDARD.decode(&receipt_base64).unwrap();
    let receipt = bincode::deserialize(&receipt_bin).unwrap();
    let isok = blindr_zk_driver::verify(&receipt);
    Ok(isok)
}

#[pymodule]
fn libblindr(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyBlindRequest>()?;

    m.add_function(wrap_pyfunction!(server_generate_keypair, m)?)?;
    m.add_function(wrap_pyfunction!(server_generate_session, m)?)?;
    m.add_function(wrap_pyfunction!(client_new_blind_request, m)?)?;
    m.add_function(wrap_pyfunction!(server_sign, m)?)?;
    m.add_function(wrap_pyfunction!(client_unblind_signature, m)?)?;
    m.add_function(wrap_pyfunction!(client_verify_signature, m)?)?;
    m.add_function(wrap_pyfunction!(hash_spend_constraint, m)?)?;
    m.add_function(wrap_pyfunction!(prove_message_fits_constraint, m)?)?;
    m.add_function(wrap_pyfunction!(verify_message_fits_constraint, m)?)?;

    Ok(())
}
