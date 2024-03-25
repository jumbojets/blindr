# blindr

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
- [ ] in the zkvm, the new request function should not take use values (need to be from previously generated request). this currently creates valid proof error
- [x] verifier needs to corroborate the proof's public journal with client-provided blinded signature value and constraint hash
- [ ] HARD: make non-dev-mode fast
