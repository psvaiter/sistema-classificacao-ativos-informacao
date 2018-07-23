import os
import bcrypt
import jwt

from datetime import datetime, timedelta

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
            id_token = generate_id_token(user)
            access_token = generate_access_token(user)

            resp.media = {
                'id_token': id_token,
                'access_token': access_token
            }
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


def generate_access_token(user):
    payload = {
        'iss': 'knoweak-api',
        'aud': 'knoweak-api',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=int(os.environ.get('ACCESS_TOKEN_EXPIRATION_IN_SECONDS'))),
        'sub': user.id
    }
    access_token = jwt.encode(payload, os.environ.get('ACCESS_TOKEN_SECRET'))
    return access_token.decode('utf-8')


def generate_id_token(user):
    payload = {
        'iss': 'knoweak-api',
        'aud': 'knoweak-web',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=int(os.environ.get('ID_TOKEN_EXPIRATION_IN_SECONDS'))),
        'sub': user.id,
        'name': user.full_name,
        'email': user.email
    }
    id_token = jwt.encode(payload, os.environ.get('ID_TOKEN_SECRET'))
    return id_token.decode('utf-8')
