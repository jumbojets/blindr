// #![no_main]
// #![no_std]

use risc0_zkvm::guest::env;
use blindr_common::{Transaction, Auth, Constraint};
use blindsign::request::BlindRequest;

// risc0_zkvm::guest::entry!(main);

fn main() {
    let (transaction, auth, constraint, public_value): (Transaction, Auth, Constraint, [u8; 32]) = env::read();

    // check that message fits constraint
    if !constraint.auth.verify(&auth) {
        panic!("auth doesnt match");
    }

    if transaction.amount > constraint.withdrawal_limit {
        panic!("bad withdrawal limit");
    }

    // compute the blinded_message
    let message = transaction.message();
    let (blinded_message, _) = BlindRequest::new_specific_msg(&public_value, &message).unwrap();

    // hash the constraint
    let hashed_constraint = constraint.hash();

    // commit blinded message and hashed constraint
    env::commit(&(blinded_message, hashed_constraint));
}
