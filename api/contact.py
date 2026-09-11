"""
Contact Message API
Stores Contact form submissions
"""
from flask import Blueprint
from flask_restful import Api, Resource
from model.contact import ContactMessage
from api.validation import ValidationError, get_json_body, clean_string, clean_email


contact_api = Blueprint('contact_api', __name__, url_prefix='/api/contact')
api = Api(contact_api)


class ContactAPI(Resource):
    def post(self):
        """
        Create a contact message
        Public endpoint

        Expected JSON body:
        {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "subject": "Question",        // optional
            "message": "Message body"
        }
        """
        try:
            data = get_json_body()
            contact_message = ContactMessage(
                name=clean_string(data, 'name', 120),
                email=clean_email(data),
                subject=clean_string(data, 'subject', 200, required=False),
                message=clean_string(data, 'message', 5000),
            )
        except ValidationError as e:
            return e.response()

        created = contact_message.create()
        if not created:
            return {'message': 'Failed to save contact message'}, 500
        return created.read(), 201


api.add_resource(ContactAPI, '')  # POST /api/contact
