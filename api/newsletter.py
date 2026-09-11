"""
Newsletter Subscriber API
Stores footer newsletter signups
"""
from flask import Blueprint
from flask_restful import Api, Resource
from model.newsletter import NewsletterSubscriber
from api.validation import ValidationError, get_json_body, clean_email


newsletter_api = Blueprint('newsletter_api', __name__, url_prefix='/api/newsletter')
api = Api(newsletter_api)


class NewsletterAPI(Resource):
    def post(self):
        """
        Subscribe an email address
        Public endpoint. Returns 201 for a new subscriber, 200 if already subscribed.

        Expected JSON body:
        {
            "email": "jane@example.com"
        }
        """
        try:
            email = clean_email(get_json_body())
        except ValidationError as e:
            return e.response()

        if NewsletterSubscriber.get_by_email(email):
            return {'message': 'Already subscribed', 'email': email}, 200

        # create() returns None on a unique-constraint race; the email is subscribed either way
        created = NewsletterSubscriber(email).create()
        if not created:
            return {'message': 'Already subscribed', 'email': email}, 200
        return {'message': 'Subscribed', 'email': email}, 201


api.add_resource(NewsletterAPI, '')  # POST /api/newsletter
