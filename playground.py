import os
import json
import requests
import time
from omegaconf import OmegaConf
import urllib3

urllib3.disable_warnings()


def complete_with_LLM(api_key, prompt: str, model_type: str, max_retry: int, parameters=None):
    """
    prompt: LLM input
    model_type: model type. see playgroud api /v2/info
        - "bloomz-7b1"
        - "homer-model/toxic-bert"
        - "homer-model/sym-sbert"
        - "homer-model/grammar-t5"
        - "homer-model/cefr-bert"
        - "coedit-xxl"
        - "wizardcoder-15b"
        - "codellama-13b-instruct"
        - "codellama-13b"
        - "llama2-13b"
        - "llama2-70b-chat"
        - "codellama-34b"
        - "codellama-34b-instruct"
    max_retry: max times to retry if LLM request fails
    """

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    url = f"https://mtklm-oa.mediatek.inc/llm/api/v2/tasks/wait"

    if not parameters:
        # if there are no params, use default parameters
        parameters = {
            "temperature": 0,
            "top_k": 0,
            "top_p": 0,
            "do_sample": True,
            "max_length": 16000,
            "min_length": 0,
            "num_beams": 0,
            "typical_p": 0,
            "repetition_penalty": 0,
            "num_return_sequences": 0,
            "max_time": 0,
            "max_new_tokens": 0,
            "return_output_only": False,
            "input_parameter_keys": [
                "string"
            ]
        }

    data = {
        "model_type": model_type,
        "prompt": str(prompt),
        "parameters": parameters,
        "with_detail": True,
    }

    for i in range(max_retry):
        is_good = False
        try:
            resp = requests.post(url,json=data, headers=headers, verify=False) # or SSLCertVerificationError
            is_good = resp.status_code == 200
            if not is_good:
                print('status_code = ', resp.status_code, ', retry...')
        except:
            print(f'{i}-th retry, will retry after {15 * (i+1)} sec')
            time.sleep(15 * (i+1))
        if is_good:
            break
        if i == (max_retry - 1):
            raise ValueError

    results = json.loads(resp.content.decode("utf-8")).get("task").get("outputs")
    final_output = []
    for result in results:
        output = result.get("text")
        final_output.append(output)
    return final_output


if __name__ == "__main__":
    setting = OmegaConf.load("./configs/setting.yaml")
    api_key = setting.MTK_PLAYGROUND_API_KEY
    result = complete_with_LLM(api_key, "how do I use pygame to make a game", model_type="codellama-13b", max_retry=100)
    print(result)
