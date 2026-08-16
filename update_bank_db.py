import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('MINI_MART_MYSQL_USER')
PWD = os.getenv('MINI_MART_MYSQL_PWD')
HOST = os.getenv('MINI_MART_MYSQL_HOST')
DB = os.getenv('MINI_MART_MYSQL_DB')

uri = f"mysql+pymysql://{USER}:{PWD}@{HOST}/{DB}"

print(f"Connecting to Aiven Database...")
try:
    engine = create_engine(uri, connect_args={"ssl": {}})
    with engine.connect() as conn:
        print("Adding Bank columns to users table...")
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN bank_name VARCHAR(100);"))
            conn.execute(text("ALTER TABLE users ADD COLUMN account_number VARCHAR(50);"))
            conn.execute(text("ALTER TABLE users ADD COLUMN account_name VARCHAR(100);"))
            conn.commit()
            print("✅ Success! Bank columns are now live.")
        except Exception as e:
            print(f"⚠️ Notice: {e}")
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")