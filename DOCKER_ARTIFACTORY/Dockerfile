FROM python:3.9-slim
WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y gcc make unzip && \
    pip install --no-cache-dir pyinstaller fastapi uvicorn pydantic && \
    chmod +x build.sh && \
    ./build.sh
EXPOSE 8089

CMD ["./bin/password_checker/password_checker"]
