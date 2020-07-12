FROM python:3.8-slim
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
   && apt-get -y install --no-install-recommends ffmpeg

COPY . /project
WORKDIR /project
RUN pip install -r requirements.txt

CMD python __main__.py
