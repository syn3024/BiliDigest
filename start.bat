@echo off
setlocal
cd /d %~dp0

echo ==================================================
echo   BiliDigest 启动器
echo ==================================================

:: 1. 尝试激活虚拟环境 (如果存在)
if exist ".venv\Scripts\activate.bat" (
    echo [状态] 检测到虚拟环境，正在激活...
    call .venv\Scripts\activate.bat
) else (
    echo [状态] 未检测到虚拟环境，将尝试使用全局 Python 运行...
)

:: 2. 检查 streamlit 是否安装
where streamlit >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到 streamlit。
    echo 请先运行: pip install -r requirements.txt
    pause
    exit
)

:: 3. 运行程序
echo [系统] 正在启动 Web 界面...
streamlit run app.py

pause
