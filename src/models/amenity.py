"""
Amenity related functionality
"""
from src import db
from src.models.base import Base


class Amenity(Base):
    """Amenity representation"""
    
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        self.name = name

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        new_amenity = Amenity(**data)
        db.session.add(new_amenity)
        db.session.commit()
        return new_amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        db.session.commit()
        return amenity


class PlaceAmenity(Base):
    """PlaceAmenity representation"""

    __tablename__ = 'place_amenities'

    place_id = db.Column(db.String(50), db.Foreignkey('places.id'), primary_key=True)
    amenity_id = db.Column(db.String(50), db.ForeingKey('amenities.id'), primary_key=True)

    def __init__(self, place_id: str, amenity_id: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence import repo

        place_amenities: list[PlaceAmenity] = repo.get_all("placeamenity")

        for place_amenity in place_amenities:
            if (
                place_amenity.place_id == place_id
                and place_amenity.amenity_id == amenity_id
            ):
                return place_amenity

        return None

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        return PlaceAmenity.query.filter_by(place_id=place_id, amenity_id=amenity_id).first()

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        new_place_amenity = PlaceAmenity(**data)
        db.session.add(new_place_amenity)
        db.session.commit()
        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        place_amenity = PlaceAmenity.get(place_id, amenity_id)
        if not place_amenity:
            return False

        db.session.delete(place_amenity)
        db.session.commit()
        return True

    @staticmethod
    def update(entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )
