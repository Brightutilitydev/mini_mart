import os
import uuid
from dotenv_vault import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User

load_dotenv()
user = os.getenv('MINI_MART_MYSQL_USER')
pwd = os.getenv('MINI_MART_MYSQL_PWD')
host = os.getenv('MINI_MART_MYSQL_HOST')
db = os.getenv('MINI_MART_MYSQL_DB')

uri = f"mysql+pymysql://{user}:{pwd}@{host}/{db}"
engine = create_engine(uri)
Session = sessionmaker(bind=engine)
session = Session()

ADMIN_EMAIL = "admin@foodmart.com"
ADMIN_PASSWORD = "AdminPassword123!"

print(f"Connecting to Aiven ({host})...")
admin_user = session.query(User).filter_by(email=ADMIN_EMAIL).first()

if admin_user:
    admin_user.is_admin = True
    admin_user.password = ADMIN_PASSWORD
    print("Admin found! Password securely reset and privileges granted.")
else:
    new_admin = User(
        id=str(uuid.uuid4()),
        first_name="System",
        last_name="Admin",
        email=ADMIN_EMAIL,
        whatsapp_number="0000000000",
        password=ADMIN_PASSWORD,
        is_admin=True
    )
    session.add(new_admin)
    print("Brand new Admin securely created!")

session.commit()
session.close()

print(f"\n✅ SUCCESS!")
print(f"Email: {ADMIN_EMAIL}")
print(f"Password: {ADMIN_PASSWORD}")
