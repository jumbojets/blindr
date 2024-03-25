#![doc = include_str!("../README.md")]

use hello_world_methods::{MULTIPLY_ID, MULTIPLY_ELF};
use risc0_zkvm::{default_prover, ExecutorEnv, Receipt, sha::Digest};
use blindr_common::{Transaction, Constraint};

type BlindedMessage = [u8; 32];

type Hash = [u8; 32];

pub fn prove(message: &Transaction, constraint: &Constraint, public_value: &[u8; 32]) -> (Receipt, BlindedMessage, Hash) {
    let env = ExecutorEnv::builder()
        .write(message)
        .unwrap()
        .write(constraint)
        .unwrap()
        .write(public_value)
        .unwrap()
        .build()
        .unwrap();
    
    let prover = default_prover();

    let receipt = prover.prove(env, MULTIPLY_ELF).unwrap();

    let (blinded_message, hashed_constraint): (_, Digest) = receipt.journal.decode().unwrap();

    let hashed_constraint = hashed_constraint.as_bytes().try_into().unwrap();

    (receipt, blinded_message, hashed_constraint)
}

pub fn verify(receipt: &Receipt) -> bool { // TODO: dont we need blinded message and hashed constraint?
    receipt.verify(MULTIPLY_ID).is_ok()
}
