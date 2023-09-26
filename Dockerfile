# Use an official Python runtime as a parent image
FROM python:3

RUN apt-get update && apt-get install -y \
    git \
    sudo \
    vim

RUN git clone https://github.com/steingartlab/unplugged.git
WORKDIR /unplugged
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["server.py"]