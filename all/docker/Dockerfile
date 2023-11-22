FROM python:3.10-alpine
WORKDIR /home/app

ENV TZ Asia/Tokyo

RUN apk --no-cache add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone && \
    apk --no-cache add icu-libs

COPY ./docker/requirements.txt /tmp
RUN pip install --upgrade pip &&  \
    pip install -r /tmp/requirements.txt

COPY ./src /home/app
CMD ["python3"]