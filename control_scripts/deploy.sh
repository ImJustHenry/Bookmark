#!/bin/bash
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
cd "$SCRIPT_DIR"
docker load --input "../build/bookmarkimage.tar"
docker tag bookmark:latest cosmicorigindev/bookmark:latest
docker push cosmicorigindev/bookmark:latest