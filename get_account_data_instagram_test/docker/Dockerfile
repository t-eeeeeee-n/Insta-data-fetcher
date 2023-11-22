FROM public.ecr.aws/lambda/python:3.11

ENV TZ Asia/Tokyo

COPY /get_account_data_instagram_test/docker/requirements.txt /var/task
RUN pip install -r /var/task/requirements.txt
COPY /get_account_data_instagram_test/src /var/task

CMD [ "lambda_function.lambda_handler" ]