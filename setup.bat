@echo off
setlocal enabledelayedexpansion

cd /d "c:\Users\User\Documents\Brevine Osoro Coding Desk.worktrees\agents-ticket-system-structure-admin-client"

echo Creating directories...
mkdir app 2>nul
mkdir app\core 2>nul
mkdir app\auth 2>nul
mkdir app\admin 2>nul
mkdir app\client 2>nul
mkdir app\customer 2>nul
mkdir app\templates 2>nul
mkdir app\templates\auth 2>nul
mkdir app\templates\admin 2>nul
mkdir app\templates\client 2>nul
mkdir app\templates\customer 2>nul
mkdir app\templates\components 2>nul

echo Directories created successfully!

REM Now run Python to create __init__.py files
python setup_dirs.py

pause
