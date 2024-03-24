RISC0_DEV_MODE=true cross build -r --target x86_64-apple-darwin
cp target/x86_64-apple-darwin/release/liblibblindr.dylib libblindr.so
cp libblindr.so ../sdk/
cp libblindr.so ../backend/app/
