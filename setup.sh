#!/bin/bash

# Check if the virtual environment already exists
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
else
  echo "Virtual environment 'venv' already exists."
fi
# Activate virtual environment (works for Git Bash in Windows)
source ./venv/Scripts/activate

# Check Python version and location
echo "Python version:"
python --version
echo "Python executable location:"
which python || where python
echo "Pip version:"
pip --version

# Install Py Dependencies
# source ./venv/Scripts/activate
python -m pip install -r requirements.txt

# Install Node Dependencies
cd ./wst_app/
npm i
cd ../

# Clear the terminal (Git Bash)
clear

# Start the backend in the background
# source ./venv/Scripts/activate
python st_app/backend/app.py &

# Start the frontend
# source ./venv/Scripts/activate
streamlit run st_app/frontend/0_🏠_Home.py --server.enableCORS=false --server.address=0.0.0.0 --server.port=8501
