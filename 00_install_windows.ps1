$ErrorActionPreference = "Stop"

if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "安装完成。下一步运行：.\01_run_demo_windows.ps1"
