#!/bin/bash
#sudo docker build . -t dst_airlines_api:latest -f Dockerfile.api # Optional
#sudo docker build . -t dst_airlines_dash:latest -f Dockerfile.dash # Optional
sudo docker-compose up --build -d

# Determine the name of the python binary
if command -v python3 &>/dev/null; then
    PY=python3 # for e.g. Ubuntu and Debian-based Distros
elif command -v python &>/dev/null; then
    PY=python # for e.g. fedora linux
else
    echo "Python not found"
    exit 1
fi

# Run the python files
$PY src/pandas_to_psql.py
$PY src/mongodb.py
