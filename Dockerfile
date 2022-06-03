FROM ubuntu:latest
 
COPY . ./app
WORKDIR ./app
RUN apt-get update && apt-get install -yqq \
    python3 \
    python3-pip && pip3 install fuzzywuzzy python-Levenshtein
CMD ["python3", "./smartbot/app.py"]

