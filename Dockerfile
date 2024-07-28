# use arvan cloud mirror images for installation of docker images
FROM docker.arvancloud.ir/python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./core/requirements.txt /app/

# use runflare mirror images for installation with pip 
RUN pip install -i https://mirror-pypi.runflare.com/simple --upgrade pip
RUN pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

COPY ./core /app/

CMD ["python","manage.py","runserver","0.0.0.0:8000"]