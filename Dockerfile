FROM    python:3.8-bullseye
WORKDIR /root
COPY    ./receiver ./receiver
RUN     pip install -r receiver/requirements.txt
RUN     mkdir covers
CMD     [ "python", "receiver/main.py" ]
