FROM 3.11.7-alpine3.18
RUN pip install -U pip
COPY app .
RUN pip install -r requirements.txt
RUN rm -rf .cache/pip