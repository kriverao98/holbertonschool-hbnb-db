"""
Place related functionality
"""
from src import db
from src.models.base import Base
from src.models.city import City
from src.models.user import User


class Place(Base):
    """Place representation"""

    __tablename__ = 'places'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    address = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    host_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.String(50), db.ForeignKey('cities.id'), nullable=False)
    price_per_night = db.Column(db.Integer)
    number_of_rooms = db.Column(db.Integer)
    number_of_bathrooms = db.Column(db.Integer)
    max_guests = db.Column(db.Integer)

    host = db.relationship('User', backref=db.backref('places', lazy=True))
    city = db.relationship('City', backref=db.backref('places', lazy=True))

    def __init__(self, data: dict | None = None, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        if not data:
            return

        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.address = data.get("address", "")
        self.city_id = data["city_id"]
        self.latitude = float(data.get("latitude", 0.0))
        self.longitude = float(data.get("longitude", 0.0))
        self.host_id = data["host_id"]
        self.price_per_night = int(data.get("price_per_night", 0))
        self.number_of_rooms = int(data.get("number_of_rooms", 0))
        self.number_of_bathrooms = int(data.get("number_of_bathrooms", 0))
        self.max_guests = int(data.get("max_guests", 0))

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        user = User.query.get(data["host_id"])

        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city = City.query.get(data["city_id"])

        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(data=data)
        db.session.add(new_place)
        db.session.commit()

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        place = Place.query.get(place_id)

        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        db.session.commit()

        return place
