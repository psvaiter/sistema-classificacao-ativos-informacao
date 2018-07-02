import falcon

from .utils import get_collection_page
from knoweak.models import Session, OrganizationAnalysis, OrganizationAnalysisDetail


class Collection:
    """GET the details of an analysis."""

    def on_get(self, req, resp, organization_code, analysis_id):
        """GETs a paged collection of details of a specific analysis from an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param analysis_id: The id of the analysis for which the details should be retrieved.
        """
        session = Session()
        try:
            organization_analysis = find_organization_analysis(organization_code, analysis_id, session)
            if organization_analysis is None:
                raise falcon.HTTPNotFound()

            # Build query to fetch items
            query = session \
                .query(OrganizationAnalysisDetail) \
                .join(OrganizationAnalysis) \
                .filter(OrganizationAnalysis.organization_id == organization_code) \
                .filter(OrganizationAnalysis.id == analysis_id) \
                .order_by(OrganizationAnalysis.created_on)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()


def find_organization_analysis(organization_code, analysis_id, session):
    query = session \
        .query(OrganizationAnalysis) \
        .filter(OrganizationAnalysis.organization_id == organization_code) \
        .filter(OrganizationAnalysis.id == analysis_id)
    return query.first()


def custom_asdict(dictable_model):
    return dictable_model.asdict(exclude=['organization_analysis_id'])
