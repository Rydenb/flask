"""
Volunteer Signup API
Stores Volunteer form submissions and lists them for admins
"""
from flask import Blueprint
from flask_restful import Api, Resource
from model.volunteer import VolunteerSignup
from api.authorize import token_required
from api.validation import ValidationError, get_json_body, clean_string, clean_email, clean_phone


volunteer_api = Blueprint('volunteer_api', __name__, url_prefix='/api/volunteer')
api = Api(volunteer_api)


class VolunteerAPI(Resource):
    def post(self):
        """
        Create a volunteer signup
        Public endpoint

        Expected JSON body:
        {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "619-555-0100",         // optional
            "interest": "Meal service",      // optional
            "availability": "Weekends",      // optional
            "message": "Anything else"       // optional
        }
        """
        try:
            data = get_json_body()
            signup = VolunteerSignup(
                name=clean_string(data, 'name', 120),
                email=clean_email(data),
                phone=clean_phone(data),
                interest=clean_string(data, 'interest', 200, required=False),
                availability=clean_string(data, 'availability', 200, required=False),
                message=clean_string(data, 'message', 2000, required=False),
            )
        except ValidationError as e:
            return e.response()

        created = signup.create()
        if not created:
            return {'message': 'Failed to save volunteer signup'}, 500
        return created.read(), 201

    @token_required("Admin")
    def get(self):
        """
        List all volunteer signups, newest first
        Admin only, since signups contain personal contact details
        """
        return VolunteerSignup.get_all(), 200


api.add_resource(VolunteerAPI, '')  # POST/GET /api/volunteer
