@echo off
setlocal

set ROOT=C:\Users\Admin\Desktop\PyCode
set PAGE_DIR=%ROOT%\page
set VENV_PY=%ROOT%\.venv\Scripts\python.exe
set BACKEND=%PAGE_DIR%\tts_backend.py
set HTML=%PAGE_DIR%\eye_estonian_teacher.html

cd /d "%PAGE_DIR%"

start "TTS Backend" cmd /k "%VENV_PY% %BACKEND%"

:WAIT_FOR_BACKEND
ping -n 2 127.0.0.1 > nul
curl -s http://localhost:8000/ > nul
if errorlevel 1 (
    goto WAIT_FOR_BACKEND
)

start "EYE Estonian Teacher" "http://localhost:8000/eye_estonian_teacher.html"

echo.
echo Backend started and HTML opened at http://localhost:8000/eye_estonian_teacher.html
echo Press any key to close this window.
pause > nul
