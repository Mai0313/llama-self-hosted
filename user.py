import json
import requests
import datetime


def get_input():
    user_input = input("You can ask any question to the Llama: ")
    return user_input

def get_user_input(user_input):
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "user_input": user_input,
        "time_input": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    url = "http://172.21.148.163:7787/llama"
    
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify = False)
    if response.status_code == 200:
        return response.json().get("result")
    return response.json().get("result")

if __name__ == "__main__":
    user_input = get_input()
    result = get_user_input(user_input)
    print(result)
    
