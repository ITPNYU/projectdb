from flask import Flask
from flask.ext.restless import APIManager
from projectdb.authn import login_manager, auth_func
from projectdb.config import config
from projectdb.database import Base, db_session, engine
from projectdb.models import Category, Class, Project, Tag, Term, Venue

app = Flask(__name__)
app.secret_key = config.get('secrets', 'SECRET')

# Flask-Login and authn code
login_manager.init_app(app)

# Flask-Restless API endpoints
# note: GET preprocessors pulled in via projectdb.authn.auth_func
manager = APIManager(app, session=db_session, preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func]))
category_blueprint = manager.create_api(Category, methods=['GET'], collection_name='category', url_prefix='/v1')
class_blueprint = manager.create_api(Class, methods=['GET'], url_prefix='/v1')
project_blueprint = manager.create_api(Project, methods=['GET'], url_prefix='/v1')
tag_blueprint = manager.create_api(Tag, methods=['GET'], collection_name='tag', url_prefix='/v1')
term_blueprint = manager.create_api(Term, methods=['GET'], collection_name='term', url_prefix='/v1')
venue_blueprint = manager.create_api(Venue, methods=['GET'], url_prefix='/v1')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
