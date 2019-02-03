import falcon

from knoweak.api.errors import Message, build_error
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.api.middlewares.auth import check_scope
from knoweak.api.utils import get_collection_page, patch_item
from knoweak.db import Session
from knoweak.db.models.catalog import SecurityThreat
from knoweak.db.models.organization import Organization, OrganizationSecurityThreat
from knoweak.db.models.system import RatingLevel


class Collection:
    """GET and POST security threats of an organization."""

    @falcon.before(check_scope, 'read:organizations')
    def on_get(self, req, resp, organization_code):
        """GETs a paged collection of security threats of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        """
        session = Session()
        try:
            organization = session.query(Organization).get(organization_code)
            if organization is None:
                raise falcon.HTTPNotFound()

            # Build query to fetch items
            query = session\
                .query(OrganizationSecurityThreat)\
                .join(SecurityThreat)\
                .filter(OrganizationSecurityThreat.organization_id == organization_code)\
                .order_by(SecurityThreat.name)\

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    @falcon.before(check_scope, 'manage:organizations')
    def on_post(self, req, resp, organization_code):
        """Adds a security threat to an organization.

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

            item = OrganizationSecurityThreat()
            item.organization_id = organization_code
            item.security_threat_id = req.media.get('security_threat_id')
            item.threat_level_id = req.media.get('threat_level_id')
            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()

class Item:
    """GET, PATCH and DELETE an organization security threat."""

    @falcon.before(check_scope, 'read:organizations')
    def on_get(self, req, resp, organization_code, security_threat_id):
        """GETs a single security threat of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param security_threat_id: The id of security threat to retrieve.
        """
        session = Session()
        try:
            item = find_organization_security_threat(security_threat_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()

    @falcon.before(check_scope, 'manage:organizations')
    def on_patch(self, req, resp, organization_code, security_threat_id):
        """Updates (partially) the security threat requested.
        All entities that reference the security threat will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization containing the security threat.
        :param security_threat_id: The id of security threat to be patched.
        """
        session = Session()
        try:
            security_threat = find_organization_security_threat(security_threat_id, organization_code, session)
            if security_threat is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, organization_code, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(security_threat, req.media, only=['threat_level_id'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': custom_asdict(security_threat)}
        finally:
            session.close()

    @falcon.before(check_scope, 'manage:organizations')
    def on_delete(self, req, resp, organization_code, security_threat_id):
        """Removes a security threat from an organization (hehe not really).

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param security_threat_id: The id of the security threat to be removed.
        """
        session = Session()
        try:
            item = find_organization_security_threat(security_threat_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            session.delete(item)
            session.commit()
        finally:
            session.close()


def validate_post(request_media, organization_code, session):
    errors = []

    # Validate security threat id and if it's already exists in organization
    # -----------------------------------------------------
    security_threat_id = request_media.get('security_threat_id')
    if security_threat_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='securityThreatId'))
    elif not session.query(SecurityThreat).get(security_threat_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='securityThreatId'))
    elif find_organization_security_threat(security_threat_id, organization_code, session):
        errors.append(build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name='securityThreatId'))

    # Validate exposure level id
    # -----------------------------------------------------
    threat_level_id = request_media.get('threat_level_id')
    if threat_level_id and not session.query(RatingLevel).get(threat_level_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='threatLevelId'))

    return errors


def validate_patch(request_media, organization_code, session):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate exposure level id if informed
    # -----------------------------------------------------
    if 'threat_level_id' in request_media:
        threat_level_id = request_media.get('threat_level_id')

        # This value CAN be null if informed...
        if threat_level_id and not session.query(RatingLevel).get(threat_level_id):
            errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='threatLevelId'))

    return errors


def find_organization_security_threat(security_threat_id, organization_code, session):
    query = session \
        .query(OrganizationSecurityThreat)\
        .filter(OrganizationSecurityThreat.organization_id == organization_code,
                OrganizationSecurityThreat.security_threat_id == security_threat_id)

    return query.first()


def custom_asdict(dictable_model):
    exclude = ['organization_id', 'security_threat_id']
    follow = {'security_threat': {'only': ['id', 'name']}}
    return dictable_model.asdict(follow=follow, exclude=exclude)
