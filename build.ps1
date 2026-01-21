# Build script for Windows

Write-Host "Installing PyInstaller..." -ForegroundColor Green
pip install pyinstaller

Write-Host "Building Windows binary..." -ForegroundColor Green
pyinstaller --onefile `
  --name extract_pdf_text `
  --hidden-import fitz `
  --clean `
  extract_pdf_text.py

Write-Host "Binary created: dist\extract_pdf_text.exe" -ForegroundColor Green
Get-Item dist\extract_pdf_text.exe | Select-Object Name, Length
