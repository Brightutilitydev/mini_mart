#!/usr/bin/env python3
"""Storage engine"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class Storage:
    """SQLAlchemy storage engine"""

    __engine = None
    __session = None

    def __init__(self, url="sqlite:///:memory:"):
        self.__engine = create_engine(url, pool_pre_ping=True)

    def add(self, obj):
        """Add an object to the session"""
        self.__session.add(obj)
        return obj

    def get(self, model, obj_id):
        """Fetch one object by id"""
        obj = self.__session.get(model, obj_id)
        return obj

    def all(self, model=None, base=None):
        """Fetch all objects of a model"""
        session = self.__session
        if not model:
            result = []
            models = Base.registry.mappers
            if base:
                models = base.registry.mappers
            for model in models:
                result.append(session.query(model).all())
            return result
        objs = session.query(model).all()
        return objs

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the session attribute"""
        self.__session.remove()
