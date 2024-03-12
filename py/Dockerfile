FROM python:3.12-slim
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-u", "bot.py"]