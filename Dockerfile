# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

COPY . /delay_bot_vk
WORKDIR /delay_bot_vk

RUN pip install -r src/requirements.txt

CMD ["python", "src/delay_bot_vk.py"]