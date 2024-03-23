use serde::{Serialize, Deserialize};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Transaction {
    pub sender: String,
    pub receiver: String,
    pub amount: u64,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Auth(pub Vec<(String, String)>);

impl Auth {
    pub fn verify(&self, against: &Auth) -> bool {
        for (name, field) in &self.0 {
            if !against.0.iter().any(|(a_name, a_field)| a_name == name && a_field == field) {
                return false;
            }
        }
        true
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Constraint {
    pub auth: Auth,  // must be equal
    pub withdrawal_limit: u64
}

impl Constraint {
    pub fn hash(&self) -> risc0_zkvm::sha::Digest {
        use sha2::{Digest as _, Sha256};
        let constraint_string = serde_json::to_string(self).unwrap();
        let hashed_constraint = Sha256::digest(&constraint_string.as_bytes());
        risc0_zkvm::sha::Digest::try_from(hashed_constraint.as_slice()).unwrap()
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
