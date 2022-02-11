FROM python:3.9-slim


WORKDIR /usr/src/app

RUN pip3 install --upgrade pip

RUN pip3 install  paho-mqtt   && \
    pip3 install pymodbus && \
    pip3 install numpy  && \
    pip install -U scikit-learn   


COPY sentron.py .
COPY Tags.py .
# COPY Runtime.py .
# COPY ODK_pipe_Socket_Linux.py .

CMD [ "python", "./sentron.py" ]

