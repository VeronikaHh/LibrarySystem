# Dockerfile
FROM python:3.13

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# Expose port and run the application
EXPOSE 8000
COPY ./alembic.ini /code/alembic.ini
COPY ./alembic /code/alembic
COPY ./run.sh /code/run.sh

RUN chmod +x /code/run.sh
CMD ["/code/run.sh"]