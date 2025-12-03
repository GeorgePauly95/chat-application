from engine import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT 'Hello, World!'"))
    print(result.all())

