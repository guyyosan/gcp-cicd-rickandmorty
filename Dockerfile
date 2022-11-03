FROM python:3.9
RUN pip install --upgrade pip

RUN adduser --disabled-password appuser
WORKDIR /usr/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R appuser:appuser /usr/app
USER appuser
EXPOSE 8000
CMD gunicorn -w 1 -b 0.0.0.0:8000 server:app
