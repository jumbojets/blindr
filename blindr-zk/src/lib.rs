#![doc = include_str!("../README.md")]

use hello_world_methods::{MULTIPLY_ID, MULTIPLY_ELF};
use risc0_zkvm::{default_prover, ExecutorEnv, Receipt};
use blindr_common::{Transaction, Constraint};

type Bytes32 = [u8; 32];

pub fn prove(message: &Transaction, constraint: &Constraint, public_value: &Bytes32) -> Receipt {
    let env = ExecutorEnv::builder()
        .write(message)
        .unwrap()
        .write(constraint)
        .unwrap()
        .write(public_value)
        .unwrap()
        .build()
        .unwrap();
    default_prover().prove(env, MULTIPLY_ELF).unwrap()
}

pub fn verify(receipt: &Receipt, blinded_message: &Bytes32, constraint_hash: &Bytes32) -> bool {
    let (blinded_message_journal, constraint_hash_journal): (Bytes32, Bytes32) = receipt.journal.decode().unwrap();

    receipt.verify(MULTIPLY_ID).is_ok()
        && *blinded_message == blinded_message_journal
        && *constraint_hash == constraint_hash_journal
}
