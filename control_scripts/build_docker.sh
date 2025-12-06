#!/bin/bash
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
cd "$SCRIPT_DIR"
cd ..
# Remove last build so we dont try to recursivly include the last build
rm -r ./build/*

cd build
touch bookmarkimage.tar
cd ..

docker build -t bookmarkimage:latest .
docker save -o ./build/bookmarkimage.tar bookmarkimage:latest