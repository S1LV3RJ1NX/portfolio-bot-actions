FROM python:3.8-slim

WORKDIR /app

# Install system libraries
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y gcc

# Install project dependencies
COPY ./requirements-actions.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements-actions.txt

COPY . .
RUN chmod +x /app/action_server.sh
CMD /app/action_server.sh