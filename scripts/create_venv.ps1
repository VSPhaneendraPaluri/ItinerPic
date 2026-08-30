param(
  [string]$EnvName = "venv"
)

Write-Host "Creating virtual environment in ./$EnvName..."
python -m venv $EnvName
Write-Host "Activating and installing requirements..."
& .\$EnvName\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r ..\requirements.txt
Write-Host "Done. Activate with: .\$EnvName\Scripts\Activate.ps1"
