FROM python:3.8-slim
WORKDIR /
RUN pip install kafka-python==2.0.2
COPY . .
CMD python -u $SCRIPT