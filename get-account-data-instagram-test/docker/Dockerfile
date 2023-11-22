FROM public.ecr.aws/lambda/python:3.11

ENV TZ Asia/Tokyo

COPY /docker/requirements.txt /var/task
RUN pip install -r /var/task/requirements.txt

CMD [ "lambda_function.lambda_handler" ]