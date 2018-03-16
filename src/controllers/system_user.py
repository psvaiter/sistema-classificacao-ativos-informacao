import falcon
import bcrypt
import app_constants as constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, validate_str, patch_item
from errors import Message, build_error
from models import Session, SystemUser
from datetime import datetime


class Collection:
    """GET and POST system users."""

    def on_get(self, req, resp):
        """GETs a paged collection of system users.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(SystemUser).order_by(SystemUser.created_on)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp):
        """Creates a new system user.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Copy fields from request to a SystemUser object
            item = SystemUser().fromdict(req.media, only=['email', 'full_name'])

            # Get password and hash it
            password = req.media.get('password')
            item.hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


class Item:
    """GET and PATCH a system user."""

    def on_get(self, req, resp, user_id):
        """GETs a single user by id.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param user_id: The id of user to retrieve.
        """
        session = Session()
        try:
            item = session.query(SystemUser).get(user_id)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()

    def on_patch(self, req, resp, user_id):
        """Updates (partially) the system user requested.
        All entities that reference the system user will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param user_id: The id of user to be patched.
        """
        session = Session()
        try:
            user = session.query(SystemUser).get(user_id)
            if user is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(user, req.media, only=['email', 'full_name'])

            # Update password if informed
            if 'password' in req.media:
                password = req.media.get('password')
                user.hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
                user.last_modified_on = datetime.utcnow()

            # Block / Unblock user if requested
            if 'is_blocked' in req.media:
                is_blocked = req.media.get('is_blocked')
                change_block_state(is_blocked, user)

            # Unlock if requested
            if req.media.get('unlock') is True:
                user.locked_out_on = None
                user.last_modified_on = datetime.utcnow()

            session.commit()
            resp.status = falcon.HTTP_OK
            resp.media = {'data': custom_asdict(user)}
        finally:
            session.close()


def validate_post(request_media, session):
    errors = []

    # Validate name
    # -----------------------------------------------------
    full_name = request_media.get('full_name')
    error = validate_str('fullName', full_name,
                         is_mandatory=True,
                         max_length=constants.GENERAL_NAME_MAX_LENGTH,
                         exists_strategy=exists_email(full_name, session))
    if error:
        errors.append(error)

    # Validate email
    # -----------------------------------------------------
    email = request_media.get('email')
    error = validate_str('email', email,
                         is_mandatory=True,
                         max_length=constants.EMAIL_MAX_LENGTH,
                         exists_strategy=exists_email(email, session))
    if error:
        errors.append(error)

    # Validate password
    # -----------------------------------------------------
    password = request_media.get('password')
    error = validate_str('password', password,
                         is_mandatory=True,
                         min_length=constants.PASSWORD_MIN_LENGTH)
    if error:
        errors.append(error)

    return errors


def validate_patch(request_media, session):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate name if informed
    # -----------------------------------------------------
    if 'full_name' in request_media:
        email = request_media.get('full_name')
        error = validate_str('fullName', email,
                             is_mandatory=True,
                             max_length=constants.GENERAL_NAME_MAX_LENGTH)
        if error:
            errors.append(error)

    # Validate email if informed
    # -----------------------------------------------------
    if 'email' in request_media:
        email = request_media.get('email')
        error = validate_str('email', email,
                             is_mandatory=True,
                             max_length=constants.EMAIL_MAX_LENGTH,
                             exists_strategy=exists_email(email, session))
        if error:
            errors.append(error)

    # Validate password if informed
    # -----------------------------------------------------
    if 'password' in request_media:
        password = request_media.get('password')
        error = validate_str('password', password,
                             is_mandatory=True,
                             min_length=constants.PASSWORD_MIN_LENGTH)
        if error:
            errors.append(error)

    return errors


def exists_email(email, session):
    def exists():
        return session.query(SystemUser.email) \
            .filter(SystemUser.email == email) \
            .first()
    return exists


def change_block_state(is_blocked, user):
    if is_blocked is True:
        # Block if requested
        # Date will only be changed if not already blocked
        if not user.blocked_on:
            user.blocked_on = datetime.utcnow()
            user.last_modified_on = datetime.utcnow()

    elif is_blocked is False:
        # Unblock if requested
        # Date will only be changed if not already unblocked
        if user.blocked_on:
            user.blocked_on = None
            user.last_modified_on = datetime.utcnow()


def custom_asdict(dictable_model):
    return dictable_model.asdict(exclude=['hashed_password'])
