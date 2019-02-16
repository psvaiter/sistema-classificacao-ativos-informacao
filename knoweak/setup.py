import falcon
from falcon_cors import CORS

from .api.middlewares.auth import AuthenticationMiddleware
from .api import extensions
from .api.resources import (
    department, macroprocess, process, it_service, it_asset, it_asset_category, security_threat, mitigation_control,
    organization, organization_department, organization_macroprocess, organization_process, organization_it_asset,
    organization_it_service, organization_it_service_it_asset, organization_security_threat,
    organization_it_asset_vulnerability, organization_it_asset_control,
    organization_analysis, organization_analysis_details, system, system_user, system_role, system_user_role,
    user_session
)


def get_api():
    api = falcon.API(
        middleware=[
            CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True).middleware,
            AuthenticationMiddleware(free_access_routes=['/version', '/healthCheck'])
        ]
    )
    configure_media_handlers(api)
    configure_routes(api)
    return api


def configure_media_handlers(api):
    json_handlers = {
        'application/json': extensions.JSONHandler(contract_in_camel_case=True),
        'application/json; charset=UTF-8': extensions.JSONHandler(contract_in_camel_case=True)
    }
    api.req_options.media_handlers.update(json_handlers)
    api.resp_options.media_handlers.update(json_handlers)


def configure_routes(api):
    api.add_route('/version', system.AppInfo())
    api.add_route('/healthCheck', system.HealthCheck())

    # Add routes for data in catalog
    api.add_route('/departments', department.Collection())
    api.add_route('/departments/{department_id}', department.Item())
    api.add_route('/macroprocesses', macroprocess.Collection())
    api.add_route('/macroprocesses/{macroprocess_id}', macroprocess.Item())
    api.add_route('/processes', process.Collection())
    api.add_route('/processes/{process_id}', process.Item())
    api.add_route('/itServices', it_service.Collection())
    api.add_route('/itServices/{it_service_id}', it_service.Item())
    api.add_route('/itAssets', it_asset.Collection())
    api.add_route('/itAssets/{it_asset_id}', it_asset.Item())
    api.add_route('/itAssetCategories', it_asset_category.Collection())
    api.add_route('/itAssetCategories/{it_asset_category_id}', it_asset_category.Item())
    api.add_route('/securityThreats', security_threat.Collection())
    api.add_route('/securityThreats/{security_threat_id}', security_threat.Item())
    api.add_route('/mitigationControls', mitigation_control.Collection())
    api.add_route('/mitigationControls/{mitigation_control_id}', mitigation_control.Item())

    # Add routes to handle organizations and their sub-resources
    api.add_route('/organizations', organization.Collection())
    api.add_route('/organizations/{organization_code}', organization.Item())
    api.add_route('/organizations/{organization_code}/departments', organization_department.Collection())
    api.add_route('/organizations/{organization_code}/departments/{department_id}', organization_department.Item())
    api.add_route('/organizations/{organization_code}/macroprocesses', organization_macroprocess.Collection())
    api.add_route('/organizations/{organization_code}/macroprocesses/{macroprocess_instance_id}', organization_macroprocess.Item())
    api.add_route('/organizations/{organization_code}/processes', organization_process.Collection())
    api.add_route('/organizations/{organization_code}/processes/{process_instance_id}', organization_process.Item())
    api.add_route('/organizations/{organization_code}/itServices', organization_it_service.Collection())
    api.add_route('/organizations/{organization_code}/itServices/{it_service_instance_id}', organization_it_service.Item())
    api.add_route('/organizations/{organization_code}/itServices/{it_service_instance_id}/itAssets', organization_it_service_it_asset.Collection())
    api.add_route('/organizations/{organization_code}/itServices/{it_service_instance_id}/itAssets/{it_asset_instance_id}', organization_it_service_it_asset.Item())
    api.add_route('/organizations/{organization_code}/itAssets', organization_it_asset.Collection())
    api.add_route('/organizations/{organization_code}/itAssets/{it_asset_instance_id}', organization_it_asset.Item())
    api.add_route('/organizations/{organization_code}/itAssets/{it_asset_instance_id}/vulnerabilities', organization_it_asset_vulnerability.Collection())
    api.add_route('/organizations/{organization_code}/itAssets/{it_asset_instance_id}/vulnerabilities/{security_threat_id}', organization_it_asset_vulnerability.Item())
    api.add_route('/organizations/{organization_code}/itAssets/{it_asset_instance_id}/controls', organization_it_asset_control.Collection())
    api.add_route('/organizations/{organization_code}/itAssets/{it_asset_instance_id}/controls/{control_id}', organization_it_asset_control.Item())
    api.add_route('/organizations/{organization_code}/securityThreats', organization_security_threat.Collection())
    api.add_route('/organizations/{organization_code}/securityThreats/{security_threat_id}', organization_security_threat.Item())
    api.add_route('/organizations/{organization_code}/analyses', organization_analysis.Collection())
    api.add_route('/organizations/{organization_code}/analyses/{analysis_id}', organization_analysis.Item())
    api.add_route('/organizations/{organization_code}/analyses/{analysis_id}/details', organization_analysis_details.Collection())

    # Routes for system user and access control
    api.add_route('/user/roles', system_role.Collection())
    api.add_route('/user/roles/{role_id}', system_role.Item())
    api.add_route('/user/users', system_user.Collection())
    api.add_route('/user/users/{user_id}', system_user.Item())
    api.add_route('/user/users/{user_id}/roles/{role_id}', system_user_role.Item())
    api.add_route('/login', user_session.Login())
