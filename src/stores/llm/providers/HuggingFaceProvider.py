# from ...LLMInterface import LLMInterface
# import logging
# from ...LLMEnums import OpenAIEnums
# from huggingface_hub import InferenceClient, InferenceTimeoutError

# class HuggingFaceProvider(LLMInterface):
#     def __init__(self, api_key: str,
#                  default_generation_max_tokens: int = 1000,
#                  default_generation_temperature: float = 0.7):
        
#         self.api_key = api_key
#         self.default_generation_max_tokens = default_generation_max_tokens
#         self.default_generation_temperature = default_generation_temperature

#         self.generation_model_id = None
#         self.embedding_model_id = None
#         self.embedding_size = None

#         self.client = InferenceClient(token=self.api_key)

#         self.logger = logging.getLogger(__name__)

#     def set_generation_model(self, model_id: str):
#         self.generation_model_id = model_id

#     def set_embedding_model(self, model_id: str, embedding_size: int):
#         self.embedding_model_id = model_id
#         self.embedding_size = embedding_size

#     def format_chat_history(self, messages: list):
#         formatted = []
#         for msg in messages:
#             role = msg["role"].lower()
#             content = self.process_text(msg["content"])
            
#             if role == OpenAIEnums.SYSTEM.value:
#                 formatted.append(f"<SYS>{content}</SYS>")
#             elif role == OpenAIEnums.USER.value:
#                 formatted.append(f"[INST]{content}[/INST]")
#             elif role == OpenAIEnums.ASSISTANT.value:
#                 formatted.append(f"{content}")

#         return "\n".join(formatted)

#     def generate_text(self, prompt: str, chat_history: list=[], 
#                     max_output_tokens: int = None,
#                     temperature: float = None):
        
#         try:
#             if not self.client:
#                 self.logger.error("HuggingFace client was not set properly")
#                 return None
            
#             if not self.generation_model_id:
#                 self.logger.error("HuggingFace generation model was not set properly")
#                 return None

#             max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_tokens
#             temperature = temperature if temperature else self.default_generation_temperature
            
#             chat_history.append(
#             self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value)
#             )

#             formatted_prompt = self.format_chat_history(chat_history)

#             response = self.client.text_generation(
#             prompt=formatted_prompt,
#             model=self.generation_model_id,
#             temperature=temperature or self.default_generation_temperature,
#             max_new_tokens=max_output_tokens or self.default_generation_max_tokens,
#             return_full_text=False,
#             )

#             if not response or not isinstance(response, str):
#                 self.logger.error(f"Error while generating response with {self.generation_model_id}")
#                 return None


#             return response.strip()
        
#         except InferenceTimeoutError as e:
#             self.logger.error("huggingface API timeout error")
#             return None
#         except Exception as e:
#             self.logger.error("Generation error")
#             return None
        


#     def embed_text(self, text: str, document_type: str = None):
#         if not self.client:
#             self.logger.error("HuggingFace client was not set properly")
#             return None
        
#         if not self.embedding_model_id:
#             self.logger.error("HuggingFace embedding model was not set properly")
#             return None
        
#         response = self.client.feature_extraction(text=text, model=self.embedding_model_id)

#         if not response or not isinstance(response, list) or len(response) == 0:
#             self.logger.error(f"Error while embedding text with {self.embedding_model_id}")
#             return None

#         return response


#     def construct_prompt(self, prompt: str, role: str):
#         return {"role": role, "content": prompt.strip()}


