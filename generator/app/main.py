from llama_cpp import Llama
from os import environ
from flask import Flask, request
from boto3 import client
from boto3.s3.transfer import TransferConfig
from datetime import datetime


class InferMixins:
    def log(self, message: str = ''):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

    def load_model(self, model_path: str = '/var/model/ggml-model-f16.gguf', gpu: bool = True):
        self.ngpu = 0
        if gpu is True:
            self.ngpu = -1
        self.model = Llama(model_path=model_path,
                           n_gpu_layers=self.ngpu)

    def run_prompt(self, prompt: str = 'Name the planets in the solar system?'):
        self.output = self.model(f"Q: {prompt} A: ",
                                 max_tokens=0,
                                 stop=["Q:"],
                                 echo=True,
                                 stream=True)

    def extract_outupt(self, output: str):
        return output['choices'][0]['text']

    def print_token(self, token: str):
        print(self.extract_outupt(token), end='')

    def stream_output(self):
        for token in self.output:
            self.print_token(token)

    def stream_to_buffer(self):
        buffer = ''
        ntoken = 0
        for token in self.output:
            buffer += self.extract_outupt(token)
            ntoken += 1
        print(f"Generated {ntoken} Tokens")
        return buffer

    def download_model(self):
        config = TransferConfig(
            multipart_threshold=1024 * 1024 * 512,
            max_concurrency=8,
            multipart_chunksize=1024 * 1024 * 512,
            use_threads=True
        )
        self.s3_client = client(
            's3',
            aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'],
            endpoint_url=f"https://accel-object.{environ['BUCKET_REGION']}.coreweave.com",
            region_name='default'
            )
        file = open('/var/model/ggml-model-f16.gguf', 'wb')
        response = self.s3_client.download_fileobj(environ['BUCKET_NAME'],
                                                   environ['FILE_NAME'],
                                                   file,
                                                   Config=config)
        print(response)


class InferMain(InferMixins):
    def __init__(self,
                 model_path: str = '/var/model/ggml-model-f16.gguf',
                 gpu: bool = True):
        self.download_model()
        self.load_model(model_path, gpu)


app = Flask(__name__)
infer = InferMain()


@app.route('/', methods=['POST'])
def serve_buffer():
    infer.log(f"Running prompt: {request.form.get('prompt')}")
    infer.run_prompt(request.form.get('prompt'))
    generated_text = infer.stream_to_buffer()
    infer.log(f"Generated text: {generated_text}")
    return generated_text


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=int(environ.get('APP_PORT', 8080)))
