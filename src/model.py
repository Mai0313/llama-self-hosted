from transformers import AutoTokenizer
import transformers
import torch
import rootutils
from omegaconf import OmegaConf

rootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)


model_selection = "meta-llama/Llama-2-7b-chat-hf"
# model_selection = "meta-llama/Llama-2-13b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_selection, cache_dir = "./models")
pipeline = transformers.pipeline(
    "text-generation",
    model=model_selection,
    torch_dtype=torch.float16,
    device_map="auto",
)

def generate_response(input_text):
    sequences = pipeline(
        input_text,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=200,
    )
    for seq in sequences:
        return f"Result: {seq['generated_text']}"

if __name__ == "__main__":
    input_text = 'I liked "Breaking Bad" and "Band of Brothers". Do you have any recommendations of other shows I might like?\n'
    result = generate_response(input_text)
    print(result)
