#!/usr/bin/env python3
"""Base Model"""

import models
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class for all models"""
    pass


class BaseModel:
    """Common properties to be inherited by all models"""

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    

    def to_dict(self):
        """Return dict representation of the model"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            **{
                c.name: getattr(self, c.name)
                for c in self.__table__.columns
                if c.name not in {"id", "created_at", "last_modified"}
            }
        }

    def save(self):
        """Update model last_modified"""
        self.last_modified = datetime.utcnow()
        models.storage.add(self)
        models.storage.save()


    def delete(self):
        """Delete user from current session"""
        models.storage.delete(self)


    def __repr__(self):
        """Readable string representation for debugging"""
        return (
            f"<{self.__class__.__name__}(id={self.id}, "
            f"created_at={self.created_at}, last_modified={self.last_modified})>"
        )
