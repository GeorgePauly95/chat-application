from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

dialect = os.getenv("dialect")
driver = os.getenv("driver")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
dbname = os.getenv("dbname")

engine = create_engine(
    f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{dbname}", echo=True
)
