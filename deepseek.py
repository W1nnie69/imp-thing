import requests
import json
from api_key import key

def build_request(message):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
        {
            "role": "user",
            "content": f"The text below are taken from a student's notes. With the text in mind, can you suggest what else can the student can write notes on."
        },
        {
            "role": "user",
            "content": f"{message}"
        }
        ],
        
    })
    )

    if response.status_code == 200:
        result = response.json()
        # The result should have a 'choices' list with message content inside
        message_content = result['choices'][0]['message']['content']
        print(message_content)
        return message_content
    else:
        print(f"Error {response.status_code}: {response.text}")
        return 