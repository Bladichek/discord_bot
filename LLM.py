from dotenv import load_dotenv
from gigachat import GigaChat
import os
import json


class Model():
    load_dotenv()

    def __init__(self) -> None:
        self.key = os.getenv('GIGACHAT_CREDENTIALS')
        if not self.key:
            raise ValueError('Не найден токен')

    def chat(self, text):
        b = GigaChat(credentials=self.key, verify_ssl_certs=True, model='GigaChat-2', ca_bundle_file="russian_trusted_root_ca.cer")
        prompt = text
        answer = b.chat(prompt)
        return answer.choices[0].message.content



def ask_LLM(text):
    model = Model()
    raw = model.chat(text)
    return raw




