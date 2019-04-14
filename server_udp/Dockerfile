FROM python:alpine3.7
WORKDIR /usr/src/app
ENV PYHTONUNBUFFERED 1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app
CMD ["python","./serverudp.py"]
EXPOSE 5005
