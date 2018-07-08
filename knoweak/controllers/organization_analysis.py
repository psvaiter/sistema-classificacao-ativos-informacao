import falcon

import app_constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, validate_str
from knoweak.models import Session, Organization, OrganizationAnalysis, OrganizationITAsset, OrganizationITService, \
    OrganizationProcess, OrganizationMacroprocess, OrganizationDepartment, OrganizationAnalysisDetail, \
    OrganizationITServiceITAsset, OrganizationITAssetVulnerability, OrganizationSecurityThreat


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
            organization = session.query(Organization).get(organization_code)
            if organization is None:
                raise falcon.HTTPNotFound()

            query = session\
                .query(OrganizationAnalysis) \
                .filter(OrganizationAnalysis.organization_id == organization_code) \
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
            item.total_processed_items = process_analysis(session, item, organization_code)

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


def process_analysis(session, analysis, organization_id, scopes=None):
    query = session\
        .query(OrganizationITServiceITAsset,
               OrganizationProcess,
               OrganizationMacroprocess,
               OrganizationDepartment,
               OrganizationSecurityThreat,
               OrganizationITAssetVulnerability)\
        .join(OrganizationITAsset)\
        .join(OrganizationITService)\
        .join(OrganizationProcess)\
        .join(OrganizationMacroprocess)\
        .join(OrganizationDepartment)\
        .join(Organization)\
        .join(OrganizationSecurityThreat)\
        .join(OrganizationITAssetVulnerability)\
        .filter(OrganizationITServiceITAsset.relevance_level_id > 0)\
        .filter(OrganizationITService.relevance_level_id > 0)\
        .filter(OrganizationProcess.relevance_level_id > 0) \
        .filter(OrganizationSecurityThreat.threat_level_id > 0) \
        .filter(OrganizationITAssetVulnerability.vulnerability_level_id > 0) \
        .filter(Organization.id == organization_id)

    result = query.all()
    total_processed_items = 0
    for item in result:
        detail = OrganizationAnalysisDetail()

        # Get the names to consolidate
        detail.it_asset_name = item.OrganizationITServiceITAsset.it_asset.name
        detail.it_service_name = item.OrganizationITServiceITAsset.it_service.name
        detail.process_name = item.OrganizationProcess.process.name
        detail.macroprocess_name = item.OrganizationMacroprocess.macroprocess.name
        detail.department_name = item.OrganizationDepartment.department.name
        detail.security_threat_name = item.OrganizationSecurityThreat.security_threat.name

        # Get the relevance, vulnerability and threat levels for calculations
        detail.it_asset_relevance = item.OrganizationITServiceITAsset.relevance_level_id
        detail.it_service_relevance = item.OrganizationITServiceITAsset.it_service_instance.relevance_level_id
        detail.process_relevance = item.OrganizationProcess.relevance_level_id
        detail.security_threat_level = item.OrganizationSecurityThreat.threat_level_id
        detail.it_asset_vulnerability_level = item.OrganizationITAssetVulnerability.vulnerability_level_id

        # Calculate risk (R = Impact * Probability)
        detail.calculated_impact = (detail.it_asset_relevance / 5) * (detail.it_service_relevance / 5) * (detail.process_relevance / 5)
        detail.calculated_probability = (detail.it_asset_vulnerability_level / 5) * (detail.security_threat_level / 5)
        detail.calculated_risk = detail.calculated_impact * detail.calculated_probability

        analysis.details.append(detail)
        total_processed_items += 1

    return total_processed_items


def custom_asdict(dictable_model):
    return dictable_model.asdict(include=['total_processed_items'], exclude=['organization_id'])
