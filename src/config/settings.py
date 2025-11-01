import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
