from flask.ext.login import LoginManager, current_user
from flask.ext.restless import ProcessingException
from projectdb.config import config

# Flask-Login user class, authenticated via API key
class APIUser(object):
    api_key = None

    def is_authenticated(self):
        if self.api_key != None:
            return True
        else:
            return False

    def is_active(self):
        if self.api_key != None:
            return True
        else:
            return False

    def is_anonymous(self):
        if self.api_key != None:
            return False
        else:
            return True

    def is_anonymous(self):
        if self.api_key != None:
            return False
        else:
            return True

    def get_id(self):
        if self.api_key != None:
            return self.api_key
        else:
            return None

    def __init__(self, a):
        self.api_key = unicode(a)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(userid):
    if userid == config.get('key', 'KEY'):
        user = APIUser(userid)
        return user
    else:
        return None

@login_manager.request_loader
def load_api_key(request):
    api_key = unicode(request.args.get('key'))
    if api_key == config.get('key', 'KEY'):
        user = APIUser(api_key)
        return user
    else:
        return None

# preprocessor for all GET requests
def auth_func(*args, **kwargs):
    if not current_user.is_authenticated():
        raise ProcessingException(description='Not authenticated!', code=401)
