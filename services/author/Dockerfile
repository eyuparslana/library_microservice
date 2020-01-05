FROM python:3.6
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN python3 -m venv flask
RUN flask/bin/pip3 install -r requirements.txt
CMD flask/bin/python3 author_controller.py