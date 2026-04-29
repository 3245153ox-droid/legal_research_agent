$ErrorActionPreference = "Stop"

if (!(Test-Path ".venv")) {
    Write-Host "未发现虚拟环境，先运行安装脚本。"
    .\00_install_windows.ps1
}

.\.venv\Scripts\Activate.ps1
python run_agent.py --topic "新就业形态劳动者权益保障研究" --input samples --out outputs

Write-Host "运行完成。请查看 outputs 文件夹。"
