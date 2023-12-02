FROM python:3-slim
COPY . .
RUN pip install -r requirements.txt
RUN rm -rf .cache/pip
ENTRYPOINT ["python","main.py"]