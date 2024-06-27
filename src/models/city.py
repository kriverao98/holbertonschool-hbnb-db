"""
City related functionality
"""

from src import db
from src.models.base import Base
from src.models.country import Country


class City(Base):
    """City representation"""
    
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(10), db.ForeignKey('countries.code'), nullable=False)

    def __init__(self, name: str, country_code: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        country = Country.query.filter_by(code=data["country_code"]).first()
        
        if not country:
            raise ValueError("Country not found")

        city = City(**data)
        db.session.add(city)
        db.session.commit()
        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Update an existing city"""
        city = City.query.get(city_id)
        if not city:
            raise ValueError("City not found")
        for key, value in data.items():
            setattr(city, key, value)
        db.session.commit()

        return city
