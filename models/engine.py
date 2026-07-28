#!/usr/bin/env python3
"""Storage engine"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

# Safely load environment variables without crashing if the package is missing
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Storage:
    """SQLAlchemy storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a Storage object"""
        ENV = os.getenv('MINI_MART_ENV', 'development')
        
        if ENV == 'development':
            url = "sqlite:///local_database.db"
        else:
            USER = os.getenv('MINI_MART_MYSQL_USER')
            PWD = os.getenv('MINI_MART_MYSQL_PWD')
            HOST = os.getenv('MINI_MART_MYSQL_HOST')
            DB = os.getenv('MINI_MART_MYSQL_DB')
            
            # 🚨 BULLETPROOF FALLBACK: Prevent fatal crashes if env vars are missing
            if not all([USER, PWD, HOST, DB]):
                print("⚠️ CRITICAL: Missing Database Variables! Falling back to SQLite.")
                url = "sqlite:///fallback.db" 
            else:
                # 🚨 AIVEN STRICT FIX: PyMySQL needs SSL passed as an argument, not in the URL string
                url = f"mysql+pymysql://{USER}:{PWD}@{HOST}/{DB}"
                
        # Pass SSL securely via connect_args if connecting to Aiven
        if ENV != 'development' and "fallback.db" not in url:
            self.__engine = create_engine(url, pool_pre_ping=True, connect_args={"ssl": {}})
        else:
            self.__engine = create_engine(url, pool_pre_ping=True)

    def add(self, obj):
        self.__session.add(obj)
        return obj

    def get(self, model, obj_id):
        return self.__session.get(model, obj_id)

    def get_by_attr(self, cls, **kwargs):
        return self.__session.query(cls).filter_by(**kwargs).first()

    def all(self, model=None, base=None):
        session = self.__session
        if not model:
            result = []
            models = Base.registry.mappers
            if base:
                models = base.registry.mappers
            for m in models:
                result.extend(session.query(m).all())
            return result
        return session.query(model).all()

    def all_by_attr(self, cls, **kwargs):
        return self.__session.query(cls).filter_by(**kwargs).all()

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        self.__session.remove()

    def rollback(self):
        self.__session.rollback()