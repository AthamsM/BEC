import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
SOCIAL_DOWNLOAD_API_TOKEN = os.getenv("SOCIAL_DOWNLOAD_API_TOKEN")
FREECONVERT_API_KEY = os.getenv("FREECONVERT_API_KEY")