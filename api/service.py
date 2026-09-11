"""
Service API
Lists services for the Get Help Now page, filtered by need and location
"""
from flask import Blueprint, request
from flask_restful import Api, Resource
from model.service import Service, NEEDS, LOCATIONS
from api.validation import ValidationError, clean_choice


service_api = Blueprint('service_api', __name__, url_prefix='/api/services')
api = Api(service_api)


class ServiceListAPI(Resource):
    """
    GET API - List services, optionally filtered
    Public endpoint
    """
    def get(self):
        """
        Query parameters (both optional, case-insensitive):
            need: one of NEEDS
            location: one of LOCATIONS
        """
        try:
            need = clean_choice(request.args.get('need'), 'need', NEEDS)
            location = clean_choice(request.args.get('location'), 'location', LOCATIONS)
        except ValidationError as e:
            return e.response()

        return Service.filter(need=need, location=location), 200


class ServiceOptionsAPI(Resource):
    """
    GET API - Valid filter values, so the frontend can build its dropdowns
    Public endpoint
    """
    def get(self):
        return {'needs': NEEDS, 'locations': LOCATIONS}, 200


api.add_resource(ServiceListAPI, '')  # GET /api/services?need=...&location=...
api.add_resource(ServiceOptionsAPI, '/options')  # GET /api/services/options
