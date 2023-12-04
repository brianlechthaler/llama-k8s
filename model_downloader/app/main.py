from huggingface_hub import snapshot_download
from os import environ

hardcoded_version: str = '1c86eca4355ecc3e955a70198a7067da7858cec6'
hardcoded_model: str = 'Llama-2-70b-chat'
hardcoded_model_author: str = 'meta-llama'


snapshot_download(
    revision=hardcoded_version,
    repo_id=f"{hardcoded_model_author}/{hardcoded_model}",
    token=environ['HF_TOKEN'],
    local_dir="/opt/model",
    cache_dir='/opt/model_cache',
    local_dir_use_symlinks=False,
    resume_download=True
)
