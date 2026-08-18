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
        print("Adding 'is_super_admin' column to users table...")
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_super_admin BOOLEAN DEFAULT FALSE;"))
            
            # Upgrade masterbright02 to super admin automatically
            conn.execute(text("UPDATE users SET is_super_admin = TRUE WHERE email = 'masterbright02@gmail.com';"))
            
            conn.commit()
            print("✅ Success! Super Admin architecture is now live.")
        except Exception as e:
            print(f"⚠️ Notice: {e}")
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")
