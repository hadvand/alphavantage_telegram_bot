import os
from dotenv import load_dotenv
from pydantic import SecretStr, StrictStr
from pydantic_settings import BaseSettings

load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("KEY", None)
    api_host: StrictStr = os.getenv("HOST", None)
    api_token: SecretStr = os.getenv("TOKEN", None)


