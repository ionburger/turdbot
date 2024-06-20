FROM python:3.12-slim
RUN mkdir -p /app
RUN mkdir -p /app/bin
COPY . /app
COPY bin/storage.py /app/bin
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-u", "bot.py"]