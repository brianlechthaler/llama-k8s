from llama_cpp import Llama
from os import environ
from flask import Flask, request


class InferMixins:
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


class InferMain(InferMixins):
    def __init__(self,
                 model_path: str = '/var/model/ggml-model-f16.gguf',
                 gpu: bool = True):
        self.load_model(model_path, gpu)


app = Flask(__name__)
infer = InferMain()


@app.route('/', methods=['POST'])
def serve_buffer():
    infer.run_prompt(request.form.get('prompt'))
    return infer.stream_to_buffer()


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=int(environ.get('PORT', 8080)))
