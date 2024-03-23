// #![no_main]
// #![no_std]

use risc0_zkvm::guest::env;
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
    let hashed_constraint = constraint.hash();

    // commit blinded message and hashed constraint
    env::commit(&(blinded_message, hashed_constraint));
}
