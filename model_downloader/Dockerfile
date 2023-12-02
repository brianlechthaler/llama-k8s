FROM python:3-slim
COPY main.py .
COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN rm -rf .cache/pip
ENTRYPOINT ["python","main.py"]