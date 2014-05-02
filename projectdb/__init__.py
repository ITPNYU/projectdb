from flask import Flask
from flask.ext.restless import APIManager
#from projectdb.database import db_session
from os import path.normpath, path.join, path.abspath
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config_path = path.normpath(path.join(path.abspath(__file__), '..', '..', 'projectdb.cfg'))
config.read(config_path)

engine = create_engine(config.get('database', 'DATABASE_URI'), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from projectdb.models import Category, Class, Project, Tag, Term, Venue

def init_db():
    import projectdb.models
    Base.metadata.create_all(bind=engine)

app = Flask(__name__)

# API endpoints
manager = APIManager(app, session=db_session)
category_blueprint = manager.create_api(Category, methods=['GET'], collection_name='category', url_prefix='/v1')
class_blueprint = manager.create_api(Class, methods=['GET'], url_prefix='/v1')
project_blueprint = manager.create_api(Project, methods=['GET'], url_prefix='/v1')
tag_blueprint = manager.create_api(Tag, methods=['GET'], collection_name='tag', url_prefix='/v1')
term_blueprint = manager.create_api(Term, methods=['GET'], collection_name='term', url_prefix='/v1')
venue_blueprint = manager.create_api(Venue, methods=['GET'], url_prefix='/v1')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
