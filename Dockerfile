FROM public.ecr.aws/docker/library/python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && apt-get -y install libpq-dev
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE ${PORT}