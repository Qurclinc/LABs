from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    
    @property
    def DB_URI(self):
        return "sqlite:///database.db"
    
    @property
    def DB_URI_MIGRATIONS(self):
        return "sqlite:///instance/database.db"
    
    
settings = Settings()