"""
Review related functionality
"""

from src import db
from src.models.base import Base
from src.models.place import Place
from src.models.user import User


class Review(Base):
    """Review representation"""

    __tablename__ = 'reviews'

    place_id = db.Column(db.String(50), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String(200))
    rating = db.Column(db.Float)

    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def __init__(
        self, place_id: str, user_id: str, comment: str, rating: float, **kw
    ) -> None:
        """Dummy init"""
        super().__init__(**kw)

        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Review":
        """Create a new review"""
        user = User.query.get(data["user_id"])

        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place = Place.query.get(data["place_id"])

        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)
        db.session.add(new_review)
        db.session.commit()

        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        """Update an existing review"""
        review = Review.query.get(review_id)

        if not review:
            return None

        for key, value in data.items():
            setattr(review, key, value)

        db.session.commit()

        return review
