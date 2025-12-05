# ...existing code...
FROM python:3.13-slim-bookworm

ENV FLASK_CONTEXT=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/sysacad/.local/bin
# Asegurar que la app lea el puerto correcto
ENV PORT=5002

RUN useradd --create-home --home-dir /home/sysacad sysacad
RUN apt-get update

# Paquetes necesarios para compilación y para que WeasyPrint funcione
RUN apt-get install -y python3-dev build-essential libpq-dev python3-psycopg2 \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
    libffi-dev libxml2 libxslt1.1 libjpeg62-turbo-dev zlib1g-dev shared-mime-info \
    curl htop iputils-ping && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/sysacad

USER sysacad
RUN mkdir app

COPY ./app ./app
COPY ./app.py .

ADD requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Exponer el mismo puerto que usa la app (PORT)
EXPOSE 5002

CMD [ "python", "./app.py" ]
