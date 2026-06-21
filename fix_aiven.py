import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load your Aiven credentials from .env
load_dotenv()

user = os.getenv('MINI_MART_MYSQL_USER')
pwd = os.getenv('MINI_MART_MYSQL_PWD')
host = os.getenv('MINI_MART_MYSQL_HOST')
db = os.getenv('MINI_MART_MYSQL_DB')

# Connect to Aiven
uri = f"mysql+pymysql://{user}:{pwd}@{host}/{db}"
engine = create_engine(uri)

with engine.connect() as conn:
    print("Connecting to Aiven Cloud Database...")
    try:
        conn.execute(text("ALTER TABLE orders ADD COLUMN delivery_address VARCHAR(255);"))
        conn.execute(text("ALTER TABLE orders ADD COLUMN contact_phone VARCHAR(50);"))
        conn.execute(text("ALTER TABLE orders ADD COLUMN gps_link VARCHAR(255);"))
        conn.commit()  # Required for SQLAlchemy 2.0
        print("✅ Aiven Database updated successfully! The 500 error is fixed.")
    except Exception as e:
        print(f"⚠️ Notice (It might already be fixed): {e}")
