import string

from pydantic import BaseSettings
import random


class Settings(BaseSettings):
	api_key: str
	api_secret: str
	secret_key: str = ''.join(random.choice(string.ascii_lowercase) for i in range(24))
