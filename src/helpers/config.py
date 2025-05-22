from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    
    ALLOWED_FILE_TYPE: list
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str

    GENERATION_BACKEND  : str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    COHERE_API_KEY: str = None
    OLLAMA_API_KEY: str = None
    OLLAMA_API_URL: str = None

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    DEFAULT_INPUT_MAX_CHARACTERS: int = None
    DEFAULT_GENERATION_MAX_TOKENS: int = None
    DEFAULT_GENERATION_TEMPERATURE: float = None

    
    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str = None

    PRIMARY_LANG: str = "en"
    DEFAULT_LANG: str = "en"

    model_config = SettingsConfigDict(env_file='.env')



def get_settings():
    return Settings()
