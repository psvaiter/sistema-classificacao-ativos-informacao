import bcrypt

from datetime import datetime
from knoweak.api.utils import validate_str
from knoweak.api.errors import build_error, Message
from knoweak.api.extensions import HTTPUnprocessableEntity, HTTPUnauthorized
from knoweak.db import Session
from knoweak.db.models.user import SystemUser, SystemUserLogin


class Login:

    def on_post(self, req, resp):
        """Process login request and return access token if successful.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            errors, user = authenticate_user(req.media, session)

            # If user was found let's save some info whether the are errors or not
            if user:
                user_login = SystemUserLogin()
                user_login.system_user_id = user.id
                user_login.attempted_on = datetime.utcnow()
                user_login.was_successful = False if errors else True
                session.add(user_login)
                session.commit()

            # Now errors can be evaluated
            if errors:
                raise HTTPUnauthorized(errors)

            # Login successful
            resp.media = {'access_token': 'fake'}
        finally:
            session.close()


class Logout:

    def on_post(self, req, resp):
        """Logout a user by invalidating open session.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            # Find and delete token
            resp.media = {}
        finally:
            session.close()


def validate_post(request_media):
        errors = []

        if not request_media:
            errors.append(build_error(Message.ERR_NO_CONTENT))
            return errors

        # Validate email
        # -----------------------------------------------------
        email = request_media.get('email')
        error = validate_str('email', email, is_mandatory=True)
        if error:
            errors.append(error)
            return errors

        # Validate password
        # -----------------------------------------------------
        password = request_media.get('password')
        error = validate_str('password', password, is_mandatory=True)
        if error:
            errors.append(error)
            return errors

        return errors


def authenticate_user(request_media, session):
        errors = []

        # Validate email
        # -----------------------------------------------------
        email = request_media.get('email')
        user = session.query(SystemUser).filter(SystemUser.email == email).first()
        if not user:
            errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='email'))
            return errors, None

        # Check password
        # -----------------------------------------------------
        password = request_media.get('password')
        if not bcrypt.checkpw(password.encode('UTF-8'), user.hashed_password):
            errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='password'))
            return errors, user

        return errors, user
