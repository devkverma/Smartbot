@echo off

REM Check if venv folder exists
IF NOT EXIST venv (
    echo Virtual environment not found. Creating one...
    python -m venv venv

    echo Activating virtual environment...
    call venv\Scripts\activate.bat

    IF EXIST requirements.txt (
        echo Installing dependencies from requirements.txt...
        pip install -r requirements.txt
    ) ELSE (
        echo requirements.txt not found. Skipping dependency installation.
    )
) ELSE (
    echo Virtual environment found. Activating...
    call venv\Scripts\activate.bat
)

echo Running application...
python main.py

exit
