FROM python:3.7.7-slim
RUN pip install --upgrade pip
RUN apt update -y &&\
    apt-get install -y \
        build-essential \
        curl \
        default-libmysqlclient-dev \
        g++ \
        gcc \
        git \
        libpq-dev \
        net-tools \
        procps \
        python3-dev \
        telnet \
        vim \
        wget
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY requirements.txt requirements.txt
RUN CFLAGS="-Wno-narrowing" pip install -r requirements.txt && \
    pip install git+https://github.com/iamumairayub/scrapyd-client.git@c4575befa450aa3054c893a8895086d1fb449405

WORKDIR /django_project
COPY . /
RUN chmod +x /docker-entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/docker-entrypoint.sh", "python", "manage.py", "runserver"]
CMD ["0:8000"]
# CMD ["tail", "-f", "/dev/null"]
