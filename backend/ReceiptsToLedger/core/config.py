import os
from dotenv import load_dotenv

load_dotenv()

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://app:app@db:5432/appdb")
