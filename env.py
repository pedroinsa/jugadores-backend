from dotenv import load_dotenv
import os

load_dotenv()


TOKEN_DURATION = int(os.getenv("TOKEN_DURATION", 1200))
ALGORITHM =  os.getenv("ALGORITHM", "HS256")
SECRET =  os.getenv("SECRET")
URL_CONNECTION = os.getenv("URL_CONNECTION")
DATABASE_URL =  os.getenv("DATABASE_URL")



