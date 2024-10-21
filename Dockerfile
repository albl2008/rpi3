FROM python:3.9-slim-buster

# Install gcc and other dependencies for building wheels
RUN apt-get update && apt-get install -y gcc python3-dev libffi-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
