import os
from huggingface_hub import hf_hub_download

MODEL_DIR = "models"
MODEL_FILENAME = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
REPO_ID = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"


def ensure_model():
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, MODEL_FILENAME)

    if os.path.exists(model_path):
        print("Model already exists.")
        return model_path

    print("Model not found. Downloading Mistral GGUF...")

    downloaded_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=MODEL_FILENAME,
        local_dir=MODEL_DIR,
        local_dir_use_symlinks=False
    )

    print("Download complete.")
    return downloaded_path

