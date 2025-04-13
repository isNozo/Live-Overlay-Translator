from ollama import chat, ChatResponse
import os

class Translator:
    def __init__(self, lang='en'):
        """Initialize the translator"""
        self.ollama_model = '7shi/gemma-2-jpn-translate:2b-instruct-q8_0'


    def translate_text(self, text):
        """Translate text using the Ollama model"""
        response: ChatResponse = chat(model=self.ollama_model, messages=[
            {"role": "user", "content": "以下の英語を日本語に翻訳してください。"},
            {'role': 'user', 'content': text,},
        ])
        return response['message']['content']
