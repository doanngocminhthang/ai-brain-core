@echo off
chcp 65001 >nul
if "%~1"=="" (
    echo [HUONG DAN] Su dung: find ^<tu_khoa^>
    echo Vi du: find kien truc
    echo        find camera
    echo        find Nam
    goto :eof
)
python "%~dp0ai_brain.py" find "%*"
