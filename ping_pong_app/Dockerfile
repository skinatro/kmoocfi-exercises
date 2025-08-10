FROM python:3-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

ENV PORT=5000

EXPOSE 5000

CMD ["python","-u","./pong.py"]