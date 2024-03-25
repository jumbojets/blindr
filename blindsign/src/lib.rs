//! An implementation of ECC based blind signatures.
//!
//! # Based On Paper
//!
//! Mathematical syntax from this documentation is taken from the paper
//! [Blind Signature Scheme Based on Elliptic Curve Cryptography](pdfs.semanticscholar.org/e58a/1713858a9e18abfc05de244e.pdf).
//!
//! # Note
//!
//! This is a sans-IO implementation, meaning that no network IO for requesting
//! or granting the initiation of the protocol is provided by this crate.

// Regular imported crates
extern crate curve25519_dalek;
extern crate digest;
extern crate failure;
extern crate rand;
extern crate typenum;
extern crate subtle;

// Imported crates with used macros
#[macro_use]
extern crate failure_derive;

// The public interface
pub mod keypair;
pub mod request;
pub mod session;
pub mod signature;

/// The Result type used
pub type Result<T> = ::std::result::Result<T, Error>;

/// The Error types
#[derive(Fail, Debug)]
pub enum Error {
    #[fail(display = "failed to initialize the RNG")]
    RngInitFailed,
    #[fail(display = "failed to convert wired scalar to scalar")]
    WiredScalarMalformed,
    #[fail(display = "failed to convert wired ristretto point to ristretto point")]
    WiredRistrettoPointMalformed,
}

impl From<rand::Error> for Error {
    fn from(_: rand::Error) -> Self {
        Error::RngInitFailed
    }
}

use rand::prelude::*;
use curve25519_dalek::scalar::Scalar;

static mut SEED: Option<[u8; 32]> = None;

pub fn set_seed(seed: Option<[u8; 32]>) {
    unsafe { SEED = seed; }
}

pub trait CryptoRngCore: CryptoRng + RngCore {}
impl<T: CryptoRng + RngCore> CryptoRngCore for T {}

pub(crate) fn random_scalar() -> Scalar {
    unsafe {
        let mut rng: Box<dyn CryptoRngCore> = match SEED {
            Some(seed) => Box::new(StdRng::from_seed(seed)),
            None => Box::new(rand::thread_rng())
        };
        let mut value = [0u8; 64];
        rng.fill_bytes(&mut value);
        Scalar::from_bytes_mod_order_wide(&value)
    }
}
