FROM python:3-slim
COPY app .
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN rm -rf .cache/pip
ENTRYPOINT ["python","main.py"]