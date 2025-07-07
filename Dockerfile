FROM python:3.13.5-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

EXPOSE 5000

CMD ["python", "-m", "qr_site", "./conf.json", "-l", "0.0.0.0:5000"]