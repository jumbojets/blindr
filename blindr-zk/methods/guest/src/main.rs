// Copyright 2024 RISC Zero, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#![no_main]
#![no_std]

use risc0_zkvm::{guest::env, sha::Digest};
use sha2::{Digest as _, Sha256};

risc0_zkvm::guest::entry!(main);

struct Transaction {
    sender: String,
    receiver: String,
    amount: u64,
}

struct Auth(Vec<(String, String)>);

impl Auth {
    fn verify(&self, against: &Auth) -> true {
        for (name, field) in &self.0 {
            if !against.0.iter().any(|(a_name, a_field)| a_name == name && a_field == field) {
                return false;
            }
        }
        true
    }
}

struct Contraint {
    auth: Auth,  // must be equal
    withdrawal_limit: u64
}

fn main() {
    let (message, auth, contraint): (Transaction, Auth, Contraint) = env::read();

    // check that message fits constraint
    if !constraint.auth.verify(&auth) {
        panic!("auth doesnt match");
    }

    if message.amount > contraint.withdrawal_limit {
        panic!("bad withdrawal limit");
    }

    // compute the blinded_message
    let blinded_message = todo!();

    // hash the constraint
    let hashed_constraint = Sha256::digest(&constraint.as_bytes);
    let hashed_constraint = Digest::try_from(hashed_constraint.as_slice()).unwrap();

    // commit blinded message and hashed constraint
    env::commit(&(blinded_message, hashed_constraint));


    if false {
        // Load the first number from the host
        let a: u64 = env::read();
        // Load the second number from the host
        let b: u64 = env::read();
        // Verify that neither of them are 1 (i.e. nontrivial factors)
        if a == 1 || b == 1 {
            panic!("Trivial factors")
        }
        // Compute the product while being careful with integer overflow
        let product = a.checked_mul(b).expect("Integer overflow");
        env::commit(&product);
    }
}

// {
//     "auth": [
//       {"password" : "hello123"},
//       {"whats your mothers maiden name": "Duke"},
//       {"whats your favorite ice cream" : "vanilla"}
//     ],
//     "transaction": [
//       {"limit" : 10}
//     ]
//   }
  