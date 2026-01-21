#!/bin/bash
# Build script for Linux

set -e

echo "Installing PyInstaller..."
pip install pyinstaller

echo "Building Linux binary..."
pyinstaller --onefile \
  --name extract_pdf_text \
  --add-binary "/usr/lib/libm.so.6:." \
  --hidden-import fitz \
  --clean \
  extract_pdf_text.py

echo "Binary created: dist/extract_pdf_text"
ls -lh dist/
