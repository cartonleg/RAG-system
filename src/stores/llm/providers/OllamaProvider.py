from ..LLMInterface import LLMInterface
from ..LLMEnums import OllamaEnums
from openai import OpenAI
import logging
import requests
from helpers.config import get_settings

class OllamaProvider(LLMInterface):
    def __init__(self, api_key: str, api_url: str=None, 
                 default_input_max_characters: int=1000,
                 default_generation_max_tokens: int=1000,
                 default_generation_temperature: float=0.7):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_tokens = default_generation_max_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(api_key=self.api_key, base_url=self.api_url if self.api_url and len(self.api_url) else None)

        self.enums = OllamaEnums

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list=[],
                      max_output_tokens: int=None,
                      temperature: float = None):
        if not self.client:
            self.logger.error("OpenAI client for Ollama was not set properly")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Ollama generation model was not set properly")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=OllamaEnums.USER.value)
            )
        
        response = self.client.chat.completions.create(
            model = self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error while generating response with Ollama")
            return None
        
        return response.choices[0].message.content


    def embed_text(self, text: str, document_type: str = None):
        settings = get_settings()

        if not self.embedding_model_id:
            self.logger.error("Ollama embedding model was not set properly")

        response = requests.post(
            ((settings.OLLAMA_API_URL)[:-3] + '/api/embeddings'),
            json={
                'model': self.embedding_model_id,
                'prompt': text
            }
        )
        
        data = response.json()
        embedding = data.get('embedding')

        if not embedding or len(embedding)==0:
            self.logger.error("Error while embedding with Ollama")
            return None
        
        return embedding
    
    def construct_prompt(self, prompt: str, role: str):
        return {"role": role, "content": prompt}





