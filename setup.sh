#!/bin/bash
sudo docker build . -t dst_airlines_api:latest -f Dockerfile.api
sudo docker build . -t dst_airlines_dash:latest -f Dockerfile.dash
sudo docker-compose up --build -d