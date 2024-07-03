"""
User related functionality
"""

from src.models.base import Base
from src import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(Base):
    """User representation"""

    __tablename__ = 'users'


    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email: str, first_name: str, last_name: str, **kw):
        """Initialize the user"""
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        """String representation of the user"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_admind": self.is_admin,
        }

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks the user's password"""
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def create(user_data: dict) -> "User":
        """Create a new user"""

        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            raise ValueError("User already exists")

        new_user = User(**user_data)
        new_user.set_password(user_data["password"])
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""

        user = User.query.get(user_id)
        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "username" in data:
            user.set_password(data["password"])
        if "is_admin" in data:
            user.is_admin = data["is_admin"]

        db.session.commit()

        return user
