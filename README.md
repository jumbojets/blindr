# blindr

## the repository

### our code

- backend: code for the custodian backend
- blindr-common: common rust code across other packages
- blindr-zk: zero knowledge proof library
- libblindr: python rust interface
- sdk: python sdk to interact with custodian backend
- node-cess: attempt to use cess as custodian storage

### modified code
- blindsign: blind signatures library modified to work in the zkvm
- risc0: fork that works with python (pyo3) and fixes a couple bugs

### TODO
- [ ] in the zkvm, the new request function should not take use values (need to be from previously generated request)
- [ ] verifier needs to corroborate the public data of the proof with blinded signature value and constraint hash
- [ ] HARD: make non-dev-mode fast
