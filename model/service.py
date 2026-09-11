"""
Service Model
Programs listed on the Get Help Now page, filterable by need and location
"""
from sqlalchemy import Text
from sqlalchemy.exc import IntegrityError
from __init__ import db


# Allowed filter values. The API rejects anything else with a 400.
NEEDS = ['food', 'shelter', 'recovery', 'medical', 'job-training', 'family']
LOCATIONS = ['downtown', 'north-county', 'east-county', 'south-bay']


class Service(db.Model):
    """
    Service Model

    Represents one program a person can get help from.
    """
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(120), nullable=False)
    _description = db.Column(Text, nullable=False)
    _need = db.Column(db.String(30), nullable=False, index=True)
    _location = db.Column(db.String(30), nullable=False, index=True)
    _address = db.Column(db.String(200), nullable=True)
    _hours = db.Column(db.String(120), nullable=True)

    def __init__(self, name, description, need, location, address=None, hours=None):
        """
        Initialize a new Service

        Args:
            name: Program name
            description: What the program provides
            need: One of NEEDS
            location: One of LOCATIONS
            address: Optional street address
            hours: Optional human-readable hours
        """
        self._name = name
        self._description = description
        self._need = need
        self._location = location
        self._address = address
        self._hours = hours

    def create(self):
        """Create a new service in the database"""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        """Read service data as a dictionary"""
        return {
            'id': self.id,
            'name': self._name,
            'description': self._description,
            'need': self._need,
            'location': self._location,
            'address': self._address,
            'hours': self._hours,
        }

    def update(self, name=None, description=None, need=None, location=None, address=None, hours=None):
        """Update any provided fields"""
        try:
            if name is not None:
                self._name = name
            if description is not None:
                self._description = description
            if need is not None:
                self._need = need
            if location is not None:
                self._location = location
            if address is not None:
                self._address = address
            if hours is not None:
                self._hours = hours
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Delete the service"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def filter(need=None, location=None):
        """Get services matching the given need and/or location, sorted by name"""
        query = Service.query
        if need:
            query = query.filter_by(_need=need)
        if location:
            query = query.filter_by(_location=location)
        return [service.read() for service in query.order_by(Service._name).all()]


def initServices():
    """Initialize the services table with sample data (for testing)"""
    if Service.query.first():
        print("Services table already contains data. Skipping initialization.")
        return

    # Placeholder test data for the mimic site, not real SDRM program details
    sample_services = [
        Service(name="Hot Meals", need="food", location="downtown",
                description="Breakfast, lunch, and dinner served daily. No sign-up required.",
                hours="Daily, 7am - 7pm"),
        Service(name="Mobile Food Pantry", need="food", location="east-county",
                description="Weekly grocery distribution for individuals and families.",
                hours="Saturdays, 9am - 12pm"),
        Service(name="Emergency Shelter", need="shelter", location="downtown",
                description="Overnight beds, showers, and case management for adults.",
                hours="Check-in nightly, 5pm - 8pm"),
        Service(name="Family Shelter", need="shelter", location="south-bay",
                description="Private rooms for women and children with on-site childcare.",
                hours="Open 24 hours"),
        Service(name="Residential Recovery Program", need="recovery", location="downtown",
                description="Long-term residential program for addiction recovery.",
                hours="Intake by appointment"),
        Service(name="Recuperative Care", need="medical", location="downtown",
                description="Short-term medical respite for people discharged from the hospital.",
                hours="Referrals accepted 24 hours"),
        Service(name="Community Health Clinic", need="medical", location="north-county",
                description="Walk-in primary care and health screenings.",
                hours="Weekdays, 8am - 4pm"),
        Service(name="Job Readiness Workshops", need="job-training", location="north-county",
                description="Resume help, interview practice, and job placement support.",
                hours="Tuesdays and Thursdays, 10am - 2pm"),
        Service(name="Family Resource Center", need="family", location="south-bay",
                description="Parenting classes, school supplies, and referrals for families.",
                hours="Weekdays, 9am - 5pm"),
    ]

    for service in sample_services:
        db.session.add(service)
    db.session.commit()
    print(f"Added {len(sample_services)} sample services.")
