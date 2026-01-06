from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import redis

load_dotenv()
url = os.getenv("url")
engine = create_engine(f"{url}", echo=True)

redis_conn = redis.Redis(host="localhost", port=6379, decode_responses=True)

print(f"redis connection: {redis_conn}")
