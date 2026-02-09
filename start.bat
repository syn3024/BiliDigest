@echo off
echo ==================================================
echo   正在启动 Bilibili AI 总结工具...
echo   (首次启动可能需要几秒钟加载环境)
echo ==================================================

:: 1. 自动进入当前目录下的虚拟环境
:: 注意：如果你 PyCharm 的虚拟环境目录名不是 .venv，请修改下面的名称
set VENV_PATH=%~dp0.venv\Scripts\activate.bat

if exist "%VENV_PATH%" (
    call "%VENV_PATH%"
) else (
    echo [错误] 找不到虚拟环境文件夹 .venv。
    echo 请确保此 bat 文件放在 PyCharm 项目的根目录下。
    pause
    exit
)

:: 2. 运行 Streamlit
streamlit run app.py

pause