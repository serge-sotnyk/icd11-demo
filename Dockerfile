FROM python:3.11

WORKDIR /csum_demo
COPY req-docker-common.txt /csum_demo
COPY req-docker-torch.txt /csum_demo

RUN apt-get update -y && apt-get install -y \
    g++ \
    gcc \
    && pip install -U pip wheel --no-cache-dir \
    && pip install -r req-docker-common.txt --no-cache-dir \
    && pip install -r req-docker-torch.txt --no-cache-dir \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

COPY . .

EXPOSE 8501

CMD [ "streamlit", "run", "st_app.py" ]