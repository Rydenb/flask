"""
Newsletter Subscriber Model
Emails collected by the footer signup
"""
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from __init__ import db


class NewsletterSubscriber(db.Model):
    """
    NewsletterSubscriber Model

    Represents one subscribed email address. Stored only, never emailed.
    """
    __tablename__ = 'newsletter_subscribers'

    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(254), unique=True, nullable=False)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, email):
        """
        Initialize a new NewsletterSubscriber

        Args:
            email: Subscriber's email, already lowercased
        """
        self._email = email
        self._created_at = datetime.utcnow()

    def create(self):
        """Create a new subscriber, or return None if the email is already subscribed"""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        """Read subscriber data as a dictionary"""
        return {
            'id': self.id,
            'email': self._email,
            'createdAt': self._created_at.isoformat() if self._created_at else None,
        }

    def update(self, email=None):
        """Update the email address"""
        try:
            if email is not None:
                self._email = email
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Delete the subscriber"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_by_email(email):
        """Get a subscriber by email"""
        return NewsletterSubscriber.query.filter_by(_email=email).first()


def initNewsletterSubscribers():
    """Initialize the newsletter_subscribers table with sample data (for testing)"""
    if NewsletterSubscriber.query.first():
        print("Newsletter subscribers table already contains data. Skipping initialization.")
        return

    sample_subscribers = [
        NewsletterSubscriber(email="subscriber1@example.com"),
        NewsletterSubscriber(email="subscriber2@example.com"),
    ]

    for subscriber in sample_subscribers:
        db.session.add(subscriber)
    db.session.commit()
    print(f"Added {len(sample_subscribers)} sample newsletter subscribers.")
