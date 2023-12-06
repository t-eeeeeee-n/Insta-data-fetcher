FROM public.ecr.aws/lambda/python:3.11.2023.11.18.02

ENV TZ Asia/Tokyo

COPY /docker/requirements.txt /var/task
RUN pip install -r /var/task/requirements.txt
COPY src /var/task

CMD [ "lambda_function.lambda_handler" ]