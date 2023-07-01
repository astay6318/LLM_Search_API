import torch
from transformers import pipeline

def load_llm_model():
    generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16,
                         trust_remote_code=True, device_map="auto", return_full_text=True)
    return generate_text
