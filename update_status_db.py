import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('MINI_MART_MYSQL_USER')
PWD = os.getenv('MINI_MART_MYSQL_PWD')
HOST = os.getenv('MINI_MART_MYSQL_HOST')
DB = os.getenv('MINI_MART_MYSQL_DB')

# ✅ BUG FIX: Removed "?ssl_mode=REQUIRED" from the string
uri = f"mysql+pymysql://{USER}:{PWD}@{HOST}/{DB}"

print(f"Connecting to Aiven Database...")
try:
    # ✅ BUG FIX: Pass SSL directly into the engine args
    engine = create_engine(uri, connect_args={"ssl": {}})
    with engine.connect() as conn:
        print("Adding 'status' column to orders table...")
        try:
            # Inject the status column and default all past orders to 'Pending'
            conn.execute(text("ALTER TABLE orders ADD COLUMN status VARCHAR(50) DEFAULT 'Pending';"))
            conn.commit()
            print("✅ Success! The 'status' column is now live.")
        except Exception as e:
            print(f"⚠️ Notice: {e}")
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")