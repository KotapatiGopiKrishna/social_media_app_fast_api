from pydantic_settings import BaseSettings

#this file is used to set/configure the variable 
#and automatically check using pydantic models
class Settings(BaseSettings):
    database_hostname:str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str 
    algorithm: str
    access_token_expire_minutes: int
    
    #this is only for non-prod env to use configs dynamically
    class Config:
        env_file = ".env"
    

settings = Settings()