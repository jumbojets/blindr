use serde::{Serialize, Deserialize};
use sha2::{Digest as _, Sha256};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Transaction {
    pub sender: String,
    pub receiver: String,
    pub amount: u64,
}

impl Transaction {
    pub fn from_str(s: &str) -> Self {
        serde_json::from_str(s).unwrap()
    }

    pub fn message(&self) -> Vec<u8> {
        serde_json::to_string(&self).unwrap().as_bytes().to_vec()
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Auth(pub Vec<(String, String)>);

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Constraint {
    pub auth: Auth,  // must be equal
    pub withdrawal_limit: u64
}

impl Constraint {
    pub fn from_str(s: &str) -> Self {
        serde_json::from_str(s).unwrap()
    }

    pub fn hash(&self) -> [u8; 32] {
        let constraint_string = serde_json::to_string(self).unwrap();
        Sha256::digest(&constraint_string.as_bytes()).as_slice().try_into().unwrap()
    }
}
