#!/bin/bash

SECRETS_PATH=secrets
OPENAI_API_KEY_PATH=${SECRETS_PATH}/OPENAI_API_KEY


setup:
	pip install -r requirements.txt
	@ if [ ! -f ${OPENAI_API_KEY_PATH} ]; \
		then mkdir -p ${SECRETS_PATH}; \
		touch ${OPENAI_API_KEY_PATH}; \
		echo "Fill credentials in file ${OPENAI_API_KEY_PATH}."; \
	fi

web:
	streamlit run main.py

cli:
	python cli.py

build:
	docker compose up --build

interactive:
	docker run --rm -it -p 8501:8501 --entrypoint /bin/bash travellerchatbot-server
