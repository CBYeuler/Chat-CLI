@echo off
REM start_all.bat - builds docker server + mongo, then opens client window
cd /d "%~dp0"

REM Ensure Docker is running
echo Starting docker-compose (mongo + server)...
docker-compose up --build -d

if %ERRORLEVEL% NEQ 0 (
  echo Docker compose failed. Make sure Docker Desktop is running.
  pause
  exit /b 1
)

REM give server a few seconds to start
echo Waiting for server to boot (3s)...
timeout /t 3 /nobreak >nul

REM Start local client in a new window (uses local venv)
if not exist ".venv\Scripts\activate.bat" (
  echo Virtualenv not found - creating .venv...
  py -m venv .venv
  echo Installing requirements...
  .venv\Scripts\activate.bat & pip install -r requirements.txt
)

REM open client in new cmd window
start "" cmd /k "cd /d \"%~dp0\" & .venv\Scripts\activate.bat & echo Running client... & python -m client.cli"

echo Done. Two windows should be open: server runs inside docker, client as local window.
exit /b 0
