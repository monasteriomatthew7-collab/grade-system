@echo off

REM Go to the project folder
cd /d "C:\Projects\grade_system"

REM Start the FastAPI server
start cmd /k py -m uvicorn system_main:app --reload

REM Wait for server to start
timeout /t 5

REM Open the HTML interface
start system_index.html