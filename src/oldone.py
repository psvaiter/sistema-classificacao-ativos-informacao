import hug
import app_constants as constants
from models import Session, Organization
from marshmallow import Schema, fields


api = hug.API(__name__)
api.http.base_url = "/api"
api.http.set_input_format("application/json", hug.input_format.json_underscore)
api.http.output_format = hug.output_format.json_camelcase


@hug.post("/organizations")
def create_organization(body, response=None):
    """Creates a new Organization in database"""

    session = None
    try:
        session = Session()
        print(body)
        print(map_from_request(body).__dict__)
        is_valid, errors = validate_create_organization(body)
        if not is_valid:
            response.status = hug.falcon.HTTP_422
            return dict(success=False, errors=errors)
        organization = map_from_request(body)
        session.add(organization)
        session.commit()
        response_data = map_from_model(organization)
    finally:
        session.close()

    return dict(success=True, data=response_data)


@hug.post("/echo")
def echo(body):

    schema = MyClassSchema()
    response_data = schema.load(body)
    return schema.dump(response_data.data)


class MyClassSchema(Schema):
    trade_name = fields.Str()
    other_name = fields.Str()


def map_from_request(request):

    return Organization(**request)
    # organization = Organization(
    #     tax_id=request.get('tax_id'),
    #     legal_name=request.get('legal_name'),
    #     trade_name=request.get('trade_name')
    # )
    # return organization


def map_from_model(model):
    return dict(
        key=model.organization_id,
        tax_id=model.tax_id,
        legal_name=model.legal_name,
        trade_name=model.trade_name
    )


def validate_create_organization(request):
    errors = []

    # Tax ID is mandatory. Validate length.
    tax_id = request.get('tax_id')
    if tax_id is None:
        errors.append("Tax ID is mandatory")
    elif len(tax_id) > constants.TAX_ID_MAX_LENGTH:
        errors.append("Tax ID is above allowed limit")

    # Legal name is mandatory. Validate length.
    legal_name = request.get('legal_name')
    if legal_name is None:
        errors.append("Legal name is mandatory")
    elif len(legal_name) > constants.GENERAL_NAME_MAX_LENGTH:
        errors.append("Legal name is above allowed limit")

    # Trade name is optional. Validate length when informed.
    trade_name = request.get("trade_name")
    if trade_name is not None and len(trade_name) > constants.GENERAL_NAME_MAX_LENGTH:
        errors.append("Trade name is above allowed limit")

    status = True if not any(errors) else False
    return status, errors
