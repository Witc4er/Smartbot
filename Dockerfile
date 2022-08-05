FROM python:latest

COPY . /smartbot

WORKDIR /smartbot

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
