import os
import uuid
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.product import Product
from models.category import Category
from dotenv import load_dotenv

# ✅ SECURE FIX: Load credentials from .env instead of hardcoding
load_dotenv()
USER = os.getenv('MINI_MART_MYSQL_USER')
PWD = os.getenv('MINI_MART_MYSQL_PWD')
HOST = os.getenv('MINI_MART_MYSQL_HOST')
DB = os.getenv('MINI_MART_MYSQL_DB')

uri = f"mysql+pymysql://{USER}:{PWD}@{HOST}/{DB}"

# Beautiful Grocery Placeholders
IMG_RICE = "https://images.unsplash.com/photo-1586201375761-83865001e8ac?q=80&w=500&auto=format&fit=crop"
IMG_PASTA = "https://images.unsplash.com/photo-1551462147-37885acc36f1?q=80&w=500&auto=format&fit=crop"
IMG_NOODLES = "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?q=80&w=500&auto=format&fit=crop"
IMG_OIL = "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?q=80&w=500&auto=format&fit=crop"
IMG_SPICES = "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?q=80&w=500&auto=format&fit=crop"
IMG_BEVERAGE = "https://images.unsplash.com/photo-1563636619-e9143da7973b?q=80&w=500&auto=format&fit=crop"
IMG_CANNED = "https://images.unsplash.com/photo-1582284540020-8acbe03f4924?q=80&w=500&auto=format&fit=crop"
IMG_SOAP = "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?q=80&w=500&auto=format&fit=crop"
IMG_GROCERY = "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=500&auto=format&fit=crop"

def determine_image(name):
    """Smart function to guess the best image based on product name"""
    n = name.lower()
    if any(x in n for x in ["rice", "beans", "garri", "semovita", "wheat"]): return IMG_RICE
    if any(x in n for x in ["macaroni", "pasta", "spaghetti"]): return IMG_PASTA
    if any(x in n for x in ["indomie", "noodles"]): return IMG_NOODLES
    if "oil" in n: return IMG_OIL
    if any(x in n for x in ["maggi", "spice", "seasoning", "salt", "thyme", "curry", "onga", "nutmeg"]): return IMG_SPICES
    if any(x in n for x in ["milk", "milo", "bournvita", "tea", "coffee", "nescafe", "custard", "cornflakes", "morn"]): return IMG_BEVERAGE
    if any(x in n for x in ["tomato", "sardine", "geisha", "can"]): return IMG_CANNED
    if any(x in n for x in ["soap", "detergent", "oral", "paste", "viva", "wash"]): return IMG_SOAP
    return IMG_GROCERY

print("Connecting to Aiven Database...")
try:
    engine = create_engine(uri, connect_args={"ssl": {}})
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Scanning entire database to force-update ALL product images...\n")
    
    all_products = session.query(Product).all()
    updated_count = 0

    for prod in all_products:
        # ✅ FORCE OVERWRITE: Replaces the image URL on EVERY product
        prod.image_url = determine_image(prod.name)
        print(f"✅ Replaced Image For: {prod.name}")
        updated_count += 1

    session.commit()
    session.close()

    print(f"\n🎉 AUTOMATION COMPLETE!")
    print(f"Forcefully updated images for ALL {updated_count} products in the database.")
    print("Refresh your Storefront or Admin Dashboard to see the new images!")

except Exception as e:
    print(f"\n❌ FATAL ERROR CONNECTING TO AIVEN:")
    print(str(e))
    sys.exit(1)