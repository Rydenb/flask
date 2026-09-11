"""
Contact Message Model
Submissions from the Contact form
"""
from datetime import datetime
from sqlalchemy import Text
from sqlalchemy.exc import IntegrityError
from __init__ import db


class ContactMessage(db.Model):
    """
    ContactMessage Model

    Represents one message sent through the Contact form. Stored only, never emailed.
    """
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(120), nullable=False)
    _email = db.Column(db.String(254), nullable=False)
    _subject = db.Column(db.String(200), nullable=True)
    _message = db.Column(Text, nullable=False)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, name, email, message, subject=None):
        """
        Initialize a new ContactMessage

        Args:
            name: Sender's name
            email: Sender's email
            message: Message body
            subject: Optional subject line
        """
        self._name = name
        self._email = email
        self._message = message
        self._subject = subject
        self._created_at = datetime.utcnow()

    def create(self):
        """Create a new contact message in the database"""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        """Read contact message data as a dictionary"""
        return {
            'id': self.id,
            'name': self._name,
            'email': self._email,
            'subject': self._subject,
            'message': self._message,
            'createdAt': self._created_at.isoformat() if self._created_at else None,
        }

    def update(self, subject=None, message=None):
        """Update the subject or message"""
        try:
            if subject is not None:
                self._subject = subject
            if message is not None:
                self._message = message
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Delete the contact message"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e


def initContactMessages():
    """Initialize the contact_messages table with sample data (for testing)"""
    if ContactMessage.query.first():
        print("Contact messages table already contains data. Skipping initialization.")
        return

    sample_messages = [
        ContactMessage(name="Test Sender", email="contact1@example.com", subject="Donation drop-off",
                       message="What hours can I drop off clothing donations?"),
        ContactMessage(name="Sample Visitor", email="contact2@example.com",
                       message="Do you accept group volunteer requests from schools?"),
    ]

    for contact_message in sample_messages:
        db.session.add(contact_message)
    db.session.commit()
    print(f"Added {len(sample_messages)} sample contact messages.")
