#!/bin/bash

setup:
	pip install -r requirements.txt
	if [ ! -f .env ]; then cp .env_template .env; echo "Fill the .env file with credentials to connect."; fi

run_web:
	streamlit run main.py

run_cli:
	python cli.py
