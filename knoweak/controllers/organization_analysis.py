import falcon

import app_constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, validate_str
from knoweak.models import Session, Organization, OrganizationAnalysis


class Collection:
    """GET and POST organization analyses."""

    def on_get(self, req, resp, organization_code):
        """GETs a paged collection of analyses of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        """
        session = Session()
        try:
            item = session.query(Organization).get(organization_code)
            if item is None:
                raise falcon.HTTPNotFound()

            query = session\
                .query(OrganizationAnalysis)\
                .order_by(OrganizationAnalysis.created_on)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp, organization_code):
        """Creates a new analysis for the organization considering the already filled values
        for relevance, vulnerability and security threat levels in processes, IT services,
        IT assets and security threats.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        """
        session = Session()
        try:
            organization = session.query(Organization).get(organization_code)
            if organization is None:
                raise falcon.HTTPNotFound()

            errors = validate_post(req.media, organization_code, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            accepted_fields = ['description', 'analysis_performed_on']
            item = OrganizationAnalysis().fromdict(req.media, only=accepted_fields)
            item.organization_id = organization_code

            # TODO: process_analysis(item)

            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


def validate_post(request_media, organization_code, session):
    errors = []

    # Validate description if informed
    # -----------------------------------------------------
    description = request_media.get('description')
    error = validate_str('description', description, max_length=app_constants.GENERAL_DESCRIPTION_MAX_LENGTH)
    if error:
        errors.append(error)

    # TODO: validate datetime that analysis was performed if informed
    # Must be a valid ISO 8601 string
    # Cannot be in the future

    return errors


def custom_asdict(dictable_model):
    return dictable_model.asdict(exclude=['organization_id'])
