import falcon
from controllers import department, macroprocess, process, information_service, information_asset, \
                        organization, organization_department, organization_macroprocess, \
                        organization_process, organization_infoservice, organization_infoasset, \
                        system_user, system_user_role
# from wsgiref.simple_server import make_server

api = application = falcon.API()

# Routes for domain data
api.add_route('/departments', department.Collection())
api.add_route('/departments/{departmentId}', department.Item())
api.add_route('/macroprocesses', macroprocess.Collection())
api.add_route('/macroprocesses/{macroprocessId}', macroprocess.Item())
api.add_route('/processes', process.Collection())
api.add_route('/processes/{processId}', process.Item())
api.add_route('/informationServices', information_service.Collection())
api.add_route('/informationServices/{informationServiceId}', information_service.Item())
api.add_route('/informationAssets', information_asset.Collection())
api.add_route('/informationAssets/{informationAssetId}', information_asset.Item())

# Routes to handle organizations and their sub-resources
api.add_route('/organizations', organization.Collection())
api.add_route('/organizations/{organizationCode}', organization.Item())
api.add_route('/organizations/{organizationCode}/departments', organization_department.Collection())
api.add_route('/organizations/{organizationCode}/departments/{departmentId}', organization_department.Item())
api.add_route('/organizations/{organizationCode}/macroprocesses', organization_macroprocess.Collection())
api.add_route('/organizations/{organizationCode}/macroprocesses/{macroprocessInstanceId}', organization_macroprocess.Item())
api.add_route('/organizations/{organizationCode}/processes', organization_process.Collection())
api.add_route('/organizations/{organizationCode}/processes/{processInstanceId}', organization_process.Item())
api.add_route('/organizations/{organizationCode}/informationServices', organization_infoservice.Collection())
api.add_route('/organizations/{organizationCode}/informationServices/{serviceInstanceId}', organization_infoservice.Item())
api.add_route('/organizations/{organizationCode}/informationAssets', organization_infoasset.Collection())
api.add_route('/organizations/{organizationCode}/informationAssets/{assetInstanceId}', organization_infoasset.Item())

# Routes for system management and access control
api.add_route('/management/users', system_user.Collection())
api.add_route('/management/users/{userId}', system_user.Item())
api.add_route('/management/userRoles', system_user_role.Collection())
api.add_route('/management/userRoles/{userRoleId}', system_user_role.Item())

# if __name__ == '__main__':
#     httpd = make_server('', 8000, api)
#     print('Serving on port 8000...')
#
#     httpd.serve_forever()
