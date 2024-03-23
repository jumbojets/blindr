// #![no_main]
// #![no_std]

use risc0_zkvm::{guest::env, sha::Digest};
use sha2::{Digest as _, Sha256};
use blindr_common::{Transaction, Auth, Constraint};

// risc0_zkvm::guest::entry!(main);

fn main() {
    let (message, auth, constraint): (Transaction, Auth, Constraint) = env::read();

    // check that message fits constraint
    if !constraint.auth.verify(&auth) {
        panic!("auth doesnt match");
    }

    if message.amount > constraint.withdrawal_limit {
        panic!("bad withdrawal limit");
    }

    // compute the blinded_message
    let blinded_message = todo!();

    // hash the constraint
    let contraint_string = "".to_owned();
    let hashed_constraint = Sha256::digest(&contraint_string.as_bytes());
    let hashed_constraint = Digest::try_from(hashed_constraint.as_slice()).unwrap();

    // commit blinded message and hashed constraint
    env::commit(&(blinded_message, hashed_constraint));
}
