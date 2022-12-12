FROM python:3.8.16

WORKDIR /scraper

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./scrapingProject/workers ./workers
COPY ./scrapingProject/app.py ./app.py

EXPOSE 9201

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# test code line start
RUN sed -i '/CipherString = DEFAULT/s/^#\?/#/' /etc/ssl/openssl.cnf
# test code line end

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9201"]