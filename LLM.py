from dotenv import load_dotenv
from gigachat import GigaChat
import os
import json
from openai import OpenAI

# class Model():
#     load_dotenv()
#
#     def __init__(self) -> None:
#         self.key = os.getenv('GIGACHAT_CREDENTIALS')
#         if not self.key:
#             raise ValueError('Не найден токен')
#
#     def chat(self, text, model):
#         b = GigaChat(credentials=self.key, verify_ssl_certs=True, model=model, ca_bundle_file="russian_trusted_root_ca.cer")
#         prompt = text
#         answer = b.chat(prompt)
#         return answer.choices[0].message.content
#
#
#
# def ask_LLM(text, model_name='GigaChat-2'):
#     model = Model()
#     print(text)
#     print('-'*20)
#     raw = model.chat(text, model_name)
#     print(raw)
#     print('*'*20)
#     return raw



# load_dotenv()
# # client = OpenAI(
# #  base_url="https://api.orcarouter.ai/v1",
# # api_key=os.getenv('ORCAROUTER_API_KEY'),)
# client = OpenAI(
#  base_url="https://agentrouter.org/v1",
# api_key=os.getenv('CHINA_ROUTER'),)



load_dotenv()

from anthropic import Anthropic

client = Anthropic(
    base_url="https://agentrouter.org",
    api_key=os.getenv('CHINA_ROUTER'),
)
def ask_LLM(messages):

    resp = client.messages.create(
        model="deepseek-v4-flash",
        max_tokens=1024,
        messages=messages,
        extra_body={"thinking": {"type": "disabled"}}
    )
    for block in resp.content:
        if block.type == 'text':
            return block.text
    return ""

