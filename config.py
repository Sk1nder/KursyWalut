from dotenv import load_dotenv
from pathlib import Path
import os

base_dir = Path(__file__).resolve().parent  #ściażka do folderu zawierajcego plik cofig.py
env_file = base_dir / ".env"    #ścieżka do pliku .env
load_dotenv(env_file)   # ładowanie z pliku zmiennych środowiskowych


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
config = Config()