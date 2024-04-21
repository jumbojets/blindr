# blindr

proof-of-concept of [blind signing](https://en.wikipedia.org/wiki/Blind_signature) a message whose blinded message fit a certain set of constraints. uses a [zero-knowledge proof](https://en.wikipedia.org/wiki/Zero-knowledge_proof) to prove to the signer such constraints are met. check [`libblindr/demo.py`](https://github.com/jumbojets/blindr/blob/master/libblindr/demo.py) for a straightforward workflow demo.

this repository also inclues code to set up up a signing server and an sdk to interact with said server.

## the repository

### our code

- libblindr: python rust interface for all crypto operations (i.e. blind signatures and zero knowledge)
- backend: code for the custodian backend
- blindr-common: common rust code across other packages
- blindr-zk: zero knowledge proof library
- sdk: python sdk to interact with custodian backend
- node-cess: use cess as custodian storage

### modified code
- blindsign: blind signatures library modified to work in the zkvm
- risc0: fork that works with python (pyo3) and fixes a couple bugs

### TODO
- [x] in the zkvm, the new request function should not take use values (need to be from previously generated request). this currently creates valid proof error
- [x] verifier needs to corroborate the proof's public journal with client-provided blinded signature value and constraint hash
- [ ] HARD: make non-dev-mode fast
