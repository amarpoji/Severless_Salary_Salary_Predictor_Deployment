FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy Backend & Model
COPY app.py ${LAMBDA_TASK_ROOT}
COPY model/ ${LAMBDA_TASK_ROOT}/model/

# Copy Frontend (Crucial Step)
COPY frontend/ ${LAMBDA_TASK_ROOT}/frontend/

CMD [ "app.handler" ]