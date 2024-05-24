from dotenv import dotenv_values
from pydantic import BaseModel, PostgresDsn


class Settings(BaseModel):
    DB_URI: PostgresDsn


settings = Settings(**dotenv_values(".env"))
