import falcon

from knoweak.api import constants
from knoweak.api.errors import build_error, Message
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.api.utils import get_collection_page, validate_str, patch_item, validate_number
from knoweak.db import Session
from knoweak.db.models.organization import (
    Organization, OrganizationAnalysis, OrganizationITAsset, OrganizationITService,
    OrganizationProcess, OrganizationMacroprocess, OrganizationDepartment, OrganizationAnalysisDetail,
    OrganizationITServiceITAsset, OrganizationITAssetVulnerability, OrganizationSecurityThreat
)


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
                .order_by(OrganizationAnalysis.created_on.desc())

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

            errors = validate_post(req.media)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            scopes = remove_redundant_scopes(req.media.get('scopes'))
            accepted_fields = ['description', 'analysis_performed_on']
            item = OrganizationAnalysis().fromdict(req.media, only=accepted_fields)
            item.organization_id = organization_code
            item.total_processed_items = process_analysis(session, item, organization_code, scopes)

            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': create_response_asdict(item)}
        finally:
            session.close()


class Item:
    """GET and PATCH an organization analysis."""

    def on_get(self, req, resp, organization_code, analysis_id):
        """GETs a single analysis of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization.
        :param analysis_id: The id of the analysis to retrieve.
        """
        session = Session()
        try:
            item = find_organization_analysis(analysis_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()

    def on_patch(self, req, resp, organization_code, analysis_id):
        """Updates (only allowed properties of) an analysis.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization.
        :param analysis_id: The id of the analysis to be patched.
        """
        session = Session()
        try:
            analysis = find_organization_analysis(analysis_id, organization_code, session)
            if analysis is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(analysis, req.media, only=['description'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': custom_asdict(analysis)}
        finally:
            session.close()


def validate_post(request_media):
    errors = []

    # Validate description if informed
    # -----------------------------------------------------
    description = request_media.get('description')
    error = validate_str('description', description, max_length=constants.GENERAL_DESCRIPTION_MAX_LENGTH)
    if error:
        errors.append(error)

    # TODO: validate datetime that analysis was performed if informed
    # Must be a valid ISO 8601 string
    # Cannot be in the future

    # Validate scopes if informed
    # -----------------------------------------------------
    scopes = request_media.get('scopes')
    for i, scope in enumerate(scopes):

        scope_i = f'scopes[{i}]'

        # departmentId is the minimum scope that must be informed
        if scope.get('department_id') is None:
            errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name=f'{scope_i}.departmentId'))

        # macroprocessId cannot be null when processId is filled
        if scope.get('macroprocess_id') is None and scope.get('process_id') is not None:
            errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name=f'{scope_i}.macroprocessId'))

        # Validate if values are numbers greater than 0
        errors.append(validate_number(f'{scope_i}.departmentId', scope.get('department_id'), min_value=1))
        errors.append(validate_number(f'{scope_i}.macroprocessId', scope.get('macroprocess_id'), min_value=1))
        errors.append(validate_number(f'{scope_i}.processId', scope.get('process_id'), min_value=1))

    # Remove None's before returning
    return [err for err in errors if err is not None]


def validate_patch(request_media):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate description if informed
    # -----------------------------------------------------
    if 'description' in request_media:
        description = request_media.get('description')
        error = validate_str('description', description, max_length=constants.GENERAL_DESCRIPTION_MAX_LENGTH)
        if error:
            errors.append(error)

    return errors


def remove_redundant_scopes(requested_scopes):
    """Remove logic:
        - Look for department only items and eliminates all more specific
        - Look for department + macroprocess only items and eliminates all more specific

    :param requested_scopes: Scopes as it came from request.
    :return: The remaining scopes
    """
    if not requested_scopes:
        return None

    whole_departments = []
    whole_macroprocesses = []

    # 1st pass: collect whole departments
    # Removing now can affect indices. Also, higher levels may be after more specific ones,
    # making it difficult to go back and remove.
    for scope in requested_scopes:
        if scope.get('department_id') is not None:
            if scope.get('macroprocess_id') is None and scope.get('process_id') is None:
                whole_departments.append(scope.get('department_id'))

    # 2nd pass: remove what's already comprehended by whole departments
    for scope in requested_scopes:
        if scope.get('department_id') in whole_departments and scope.get('macroprocess_id') is not None:
            del requested_scopes[scope]

    # 3rd pass: collect whole macroprocesses
    for scope in requested_scopes:
        if scope.get('macroprocess_id') is not None and scope.get('process_id') is None:
            whole_macroprocesses.append(scope.get('macroprocess_id'))

    # 4th pass: remove what's already comprehended by whole macroprocesses
    for scope in requested_scopes:
        if scope.get('macroprocess_id') in whole_macroprocesses and scope.get('process_id') is not None:
            del requested_scopes[scope]

    return requested_scopes


def find_organization_analysis(analysis_id, organization_code, session):
    query = session \
        .query(OrganizationAnalysis) \
        .filter(OrganizationAnalysis.organization_id == organization_code) \
        .filter(OrganizationAnalysis.id == analysis_id)
    return query.first()


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

    append_filters_from_scopes(query, scopes)
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


def append_filters_from_scopes(query, scopes):
    pass


def custom_asdict(dictable_model):
    return dictable_model.asdict(exclude=['organization_id'])


def create_response_asdict(dictable_model):
    return dictable_model.asdict(include=['total_processed_items'], exclude=['organization_id'])
