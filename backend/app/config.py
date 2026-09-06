from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# this is specifically the path from where the root of where this app lives
BASE_DIR = Path(__file__).resolve().parent.parent 

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR/".env", env_file_encoding="utf-8")

    # database connection
    db_host: str
    db_port: int
    db_name: str

    # app user
    db_user: str
    db_password: str

    # admin user
    db_admin_user: str
    db_admin_password: str

    # session handling
    session_secret_key: str

    # login special code
    signup_code: str

settings = Settings()