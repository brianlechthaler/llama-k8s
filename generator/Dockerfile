ARG CUDA_IMAGE="11.7.1-devel-ubuntu22.04"
FROM nvidia/cuda:${CUDA_IMAGE}

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git build-essential \
    python3 python3-pip gcc wget

# setting build related env vars
ENV CUDA_DOCKER_ARCH=all
ENV LLAMA_CUBLAS=1

# Install depencencies
RUN python3 -m pip install --upgrade pip pytest cmake scikit-build setuptools fastapi uvicorn sse-starlette pydantic-settings starlette-context boto3

# Install llama-cpp-python (build with cuda)
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
RUN mkdir -p /opt/runtime
COPY app /opt/runtime
WORKDIR /opt/runtime
RUN mkdir -p /var/model
# Install production dependencies.
RUN pip install Flask gunicorn

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --capture-output --bind :$EXEC_PORT --workers 1 --timeout 3600 main:app