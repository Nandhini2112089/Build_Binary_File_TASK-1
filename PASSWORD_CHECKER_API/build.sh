#!/bin/bash

echo "Cleaning old builds..."
rm -rf build dist
rm -f bin/password_checker

echo "Building FastAPI app into binary..."
pyinstaller --onefile src/password_checker.py --distpath bin --name password_checker

echo "Build complete! Binary saved in bin/password_checker"
