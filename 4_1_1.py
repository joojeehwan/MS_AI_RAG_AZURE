import os
from openai import AzureOpenAI

endpoint = "https://ktds-sgsg.cognitiveservices.azure.com/"
model_name = "gpt-5-chat"
deployment = "gpt-5-chat"

subscription_key = ""
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

response = client.chat.completions.create(
    stream=True,
    messages=[
        {
            "role": "system",
            "content": "너는 친절한 도우미야. 모든 질문에 적극적으로 대답하지",
        },
        {
            "role": "user",
            "content": "방배역 근처 남부터미널역까지 근처로, 점심 맛집 추천해줘",
        }
    ],
    max_tokens=16384,
    temperature=1.0,
    top_p=1.0,
    model=deployment,
)

for update in response:
    if update.choices:
        print(update.choices[0].delta.content or "", end="")

client.close()