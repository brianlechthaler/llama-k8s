FROM python:3.9.18-slim
COPY app .
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN rm -rf .cache/pip
ENTRYPOINT ["python","main.py","/opt/model"]
