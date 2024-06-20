FROM python:3.9.1

EXPOSE 8000

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python manage.py migrate
RUN python manage.py test
ENTRYPOINT [ "python" ]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
