from datetime import datetime
from typing import Any, Optional
import uuid
from abc import ABC, abstractmethod
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from src import db


@as_declarative()
class Base(db.Model, ABC):
    """
    Abstract base class for all models
    """
    __abstract__ = True

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs) -> None:
        """
        Base class constructor. If kwargs are provided, set them as attributes.
        """
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                continue
            setattr(self, key, value)

    @classmethod
    def get(cls, id: str) -> Optional["Base"]:
        """
        Common method to get a specific object of a class by its id.
        """
        return cls.query.get(id)

    @classmethod
    def get_all(cls) -> list["Base"]:
        """
        Common method to get all objects of a class.
        """
        return cls.query.all()

    @classmethod
    def delete(cls, id: str) -> bool:
        """
        Common method to delete a specific object of a class by its id.
        """
        instance = cls.get(id)
        if not instance:
            return False
        db.session.delete(instance)
        db.session.commit()
        return True

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any:
        """Creates a new object of the class"""

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Any | None:
        """Updates an object of the class"""
