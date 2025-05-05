#!/bin/bash

echo "Cleaning old builds..."
rm -rf build dist
rm -f bin/password_checker

echo "Building FastAPI app into binary..."
pyinstaller -y src/main.py --distpath bin --name password_checker --paths=lib 

echo "Build complete! Binary saved in bin/password_checker"

