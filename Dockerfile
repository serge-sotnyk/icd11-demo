FROM python:3.11-slim-bullseye

WORKDIR /csum_demo
COPY requirements.txt /csum_demo

RUN apt-get update -y && apt-get install -y \
    g++ \
    gcc \
    && pip install -U pip wheel --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

COPY . .

EXPOSE 8501

CMD [ "streamlit", "run", "st_app.py" ]