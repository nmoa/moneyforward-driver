import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

MF_EMAIL = os.getenv('MF_EMAIL')
MF_PASSWORD = os.getenv('MF_PASSWORD')
