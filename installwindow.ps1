# Install script for Windows
# Chạy trong PowerShell: .\install_windows.ps1

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Disease Prediction Service - Windows Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.9-3.12" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install packages one by one
Write-Host ""
Write-Host "Installing packages..." -ForegroundColor Yellow

$packages = @(
    "numpy",
    "pandas",
    "scikit-learn",
    "Flask==3.0.0",
    "Flask-CORS==4.0.0",
    "joblib",
    "python-dotenv"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    pip install $package --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $package installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to install $package" -ForegroundColor Red
    }
}

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow

$verification = @"
import sys
try:
    import numpy
    import pandas
    import sklearn
    import flask
    import joblib
    print('✓ All packages imported successfully!')
    print(f'  - NumPy: {numpy.__version__}')
    print(f'  - Pandas: {pandas.__version__}')
    print(f'  - scikit-learn: {sklearn.__version__}')
    print(f'  - Flask: {flask.__version__}')
    sys.exit(0)
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"@

python -c $verification

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "Installation completed successfully!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Train model: python train_model.py" -ForegroundColor White
    Write-Host "  2. Run server: python run.py" -ForegroundColor White
    Write-Host "  3. Test API: python test_api.py" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "Installation failed. Please check errors above." -ForegroundColor Red
    Write-Host "See WINDOWS_INSTALL.md for troubleshooting." -ForegroundColor Yellow
}