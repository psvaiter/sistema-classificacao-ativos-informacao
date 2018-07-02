import falcon

from .utils import get_collection_page
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

            data, paging = get_collection_page(req, query, get_custom_asdict(req.relative_uri))

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

            accepted_fields = ['description', 'analysis_performed_on']
            item = OrganizationAnalysis().fromdict(req.media, only=accepted_fields)
            item.organization_id = organization_code

            # TODO: process_analysis(item)

            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': get_custom_asdict(req.relative_uri)(item)}
        finally:
            session.close()


def get_custom_asdict(relative_uri):
    """Returns a function that maps a model object to a dict.

    :param relative_uri: Relative URI to build the location of analysis details on final dict.
    :return: Function that receives a model an returns a dict.
    """
    def custom_asdict(analysis):
        analysis.details_location = relative_uri + f'/{analysis.id}/details'
        return analysis.asdict(include=['details_location'], exclude=['organization_id'])

    return custom_asdict
