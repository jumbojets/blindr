RISC0_DEV_MODE=true cargo build -r
cp target/release/liblibblindr.dylib libblindr.so
cp libblindr.so ../sdk/
cp libblindr.so ../backend/app/
