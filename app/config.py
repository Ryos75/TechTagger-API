from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "TechTagger"
    app_version: str = "1.0.0"
    debug: bool = True
    
    models_dir: str = "./models"
    
    use_oci_storage: bool = False
    oci_namespace: str = ""
    oci_bucket_name: str = "techtagger-models"
    oci_config_file: str = "~/.oci/config"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()