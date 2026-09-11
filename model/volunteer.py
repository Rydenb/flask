"""
Volunteer Signup Model
Submissions from the Volunteer form
"""
from datetime import datetime
from sqlalchemy import Text
from sqlalchemy.exc import IntegrityError
from __init__ import db


class VolunteerSignup(db.Model):
    """
    VolunteerSignup Model

    Represents one person offering to volunteer. Stored only, never emailed.
    """
    __tablename__ = 'volunteer_signups'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(120), nullable=False)
    _email = db.Column(db.String(254), nullable=False)
    _phone = db.Column(db.String(30), nullable=True)
    _interest = db.Column(db.String(200), nullable=True)
    _availability = db.Column(db.String(200), nullable=True)
    _message = db.Column(Text, nullable=True)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, name, email, phone=None, interest=None, availability=None, message=None):
        """
        Initialize a new VolunteerSignup

        Args:
            name: Volunteer's name
            email: Contact email
            phone: Optional phone number
            interest: Optional area they want to help with
            availability: Optional days/times they can help
            message: Optional note
        """
        self._name = name
        self._email = email
        self._phone = phone
        self._interest = interest
        self._availability = availability
        self._message = message
        self._created_at = datetime.utcnow()

    def create(self):
        """Create a new signup in the database"""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        """Read signup data as a dictionary"""
        return {
            'id': self.id,
            'name': self._name,
            'email': self._email,
            'phone': self._phone,
            'interest': self._interest,
            'availability': self._availability,
            'message': self._message,
            'createdAt': self._created_at.isoformat() if self._created_at else None,
        }

    def update(self, phone=None, interest=None, availability=None, message=None):
        """Update any provided optional fields"""
        try:
            if phone is not None:
                self._phone = phone
            if interest is not None:
                self._interest = interest
            if availability is not None:
                self._availability = availability
            if message is not None:
                self._message = message
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Delete the signup"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        """Get all signups, newest first"""
        signups = VolunteerSignup.query.order_by(VolunteerSignup._created_at.desc()).all()
        return [signup.read() for signup in signups]


def initVolunteerSignups():
    """Initialize the volunteer_signups table with sample data (for testing)"""
    if VolunteerSignup.query.first():
        print("Volunteer signups table already contains data. Skipping initialization.")
        return

    sample_signups = [
        VolunteerSignup(name="Test Volunteer", email="volunteer1@example.com",
                        interest="Meal service", availability="Weekend mornings"),
        VolunteerSignup(name="Sample Helper", email="volunteer2@example.com", phone="619-555-0100",
                        interest="Donation sorting", availability="Weekday evenings",
                        message="Happy to help with holiday events too."),
    ]

    for signup in sample_signups:
        db.session.add(signup)
    db.session.commit()
    print(f"Added {len(sample_signups)} sample volunteer signups.")
