# syntax=docker/dockerfile:1.4
FROM boltzmachine/f22-yarxiver-backend:latest AS builder

WORKDIR /code

COPY . .

WORKDIR /
RUN mv model code/backend/utils/

WORKDIR /code/frontend
RUN npm run build

WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8000
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 8000

CMD ["flask", "run"]
