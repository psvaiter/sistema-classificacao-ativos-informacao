import falcon
from .extensions import HTTPUnprocessableEntity
from errors import Message, build_error
from models import Session, SystemAdministrativeRole, SystemUser, SystemUserAdministrativeRole


class Item:
    """PUT and DELETE a system role to/from a user."""

    def on_put(self, req, resp, user_id, role_id):
        """Adds a role to a system user.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param user_id: The id of user.
        :param role_id: The id of role to be added.
        """
        session = Session()
        try:
            user = session.query(SystemUser).get(user_id)
            if user is None:
                raise falcon.HTTPNotFound()

            errors = validate_put(req.media, user_id, role_id, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Add role if not already there
            user_role = find_user_role(user_id, role_id, session)
            if not user_role:
                user_role = SystemUserAdministrativeRole(user_id=user_id, role_id=role_id)
                session.add(user_role)

            session.commit()
            resp.status = falcon.HTTP_OK
            resp.media = {'data': custom_asdict(user_role)}
        finally:
            session.close()

    def on_delete(self, req, resp, user_id, role_id):
        """Removes a role from a system user.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param user_id: The id of user.
        :param role_id: The id of role to be removed.
        """
        session = Session()
        try:
            item = find_user_role(user_id, role_id, session)
            if item is None:
                raise falcon.HTTPNotFound()

            session.delete(item)
            session.commit()
        finally:
            session.close()


def validate_put(request_media, user_id, role_id, session):
    errors = []

    # Validate role id
    # -----------------------------------------------------
    if not role_id:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='route:role_id'))
    elif not session.query(SystemAdministrativeRole).get(role_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='route:role_id'))

    return errors


def find_user_role(user_id, role_id, session):
    query = session \
        .query(SystemUserAdministrativeRole) \
        .filter(SystemUserAdministrativeRole.user_id == user_id) \
        .filter(SystemUserAdministrativeRole.role_id == role_id)
    return query.first()


def custom_asdict(dictable_model):
    exclude = ['role_id']
    include = {
        'role': {'only': ['id', 'name']}
    }
    return dictable_model.asdict(follow=include, exclude=exclude)
