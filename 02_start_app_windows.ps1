$ErrorActionPreference = "Stop"

if (!(Test-Path ".venv")) {
    Write-Host "未发现虚拟环境，先运行安装脚本。"
    .\00_install_windows.ps1
}

.\.venv\Scripts\Activate.ps1
streamlit run app.py
