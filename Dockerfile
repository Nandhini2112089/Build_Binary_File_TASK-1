FROM python:3.11

WORKDIR /app

COPY password_checker /app/password_checker

EXPOSE 8081

RUN chmod +x /app/password_checker/password_checker

ENTRYPOINT ["/app/password_checker/password_checker"]
