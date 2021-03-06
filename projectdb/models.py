from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.dialects.mysql import TINYINT
#from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from projectdb.database import Base, engine

# ORM classes
class Category(Base):
    __tablename__ = 'categories'
    __table__ = Table(__tablename__, Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<Category %r>' % (self.text)

class Class(Base):
    __tablename__ = 'class'
    __table__ = Table(__tablename__, Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<Class %r>' % (self.class_name)

class Document(Base):
    __tablename__ = 'projectDocuments'
    document_id = Column('document_id', Integer, primary_key=True)
    project_id = Column('project_id', Integer, ForeignKey('project.project_id'), nullable=False)
    document = Column('document', String, nullable=False)
    document_name = Column('document_name', String, nullable=False)
    document_type_id = Column('document_type_id', Integer, nullable=False)
    main_image = Column('main_image', Boolean, nullable=False)
    secret = Column('secret', Boolean, nullable=False)

    def __repr__(self):
        return '<Document %r>' % (self.class_name)

class Project(Base):
    __tablename__ = 'project'
    __table__ = Table(__tablename__, Base.metadata, autoload=True, autoload_with=engine)
    categories = relationship('Category', secondary='projectCategoryMap', backref='projects')
    classes = relationship('Class', secondary='classProject', backref='projects')
    documents = relationship('Document', backref='project')
    people = relationship('PeopleAssociation')
    #venues = relationship('Venue', secondary='venueProject', backref='projects')
    venues = relationship('VenueProjectAssociation', primaryjoin='and_(Project.project_id==VenueProjectAssociation.project_id, VenueProjectAssociation.approved==1)')
    venues_pending = relationship('VenueProjectAssociation', primaryjoin='and_(Project.project_id==VenueProjectAssociation.project_id, VenueProjectAssociation.approved!=1)')

    def __repr__(self):
        return '<Project %r>' % (self.project_name)

class Tag(Base):
    __tablename__ = 'tags'
    __table__ = Table(__tablename__, Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<Tag %r>' % (self.descr)

class Term(Base):
    __tablename__ = 'terms'
    __table__ = Table(__tablename__, Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<Term %r>' % (self.term)

class PeopleAssociation(Base):
    __tablename__ = 'userProject'
    point = Column('designated', Boolean, nullable=False)
    project_id = Column('project_id', Integer, ForeignKey('project.project_id'), primary_key=True)
    netid = Column('user_id', String, primary_key=True)

class Venue(Base):
    __tablename__ = 'venue'
    __table__ = Table(__tablename__, Base.metadata, autoload=True, autoload_with=engine)
    #projects = relationship('VenueProjectAssociation', backref='venues')
    projects = relationship('VenueProjectAssociation', primaryjoin='and_(Venue.venue_id==VenueProjectAssociation.venue_id, VenueProjectAssociation.approved==1)')
    projects_pending = relationship('VenueProjectAssociation', primaryjoin='and_(Venue.venue_id==VenueProjectAssociation.venue_id, VenueProjectAssociation.approved!=1)')

    def __repr__(self):
        return '<Venue %r>' % (self.venue_name)

class VenueProjectAssociation(Base):
    __tablename__ = 'venueProject'
    #__mapper_args__ = { 'exclude_properties' : ['venue_id', 'project_id'] }
    project_id = Column('project_id', Integer, ForeignKey('project.project_id'), nullable=False, primary_key=True)
    venue_id = Column('venue_id', Integer, ForeignKey('venue.venue_id'), nullable=False, primary_key=True)
    approved = Column('approved', TINYINT, nullable=False)
    venue = relationship('Venue')
    project = relationship('Project')

# association tables
class_project = Table('classProject', Base.metadata,
    Column('class_id', Integer, ForeignKey('class.class_id'), nullable=False),
    Column('project_id', Integer, ForeignKey('project.project_id'), nullable=False)
)

project_category = Table('projectCategoryMap', Base.metadata,
    Column('category_id', Integer, ForeignKey('categories.category_id'), nullable=False),
    Column('project_id', Integer, ForeignKey('project.project_id'), nullable=False)
)

#venue_project = Table('venueProject', Base.metadata,
#    Column('project_id', Integer, ForeignKey('project.project_id'), nullable=False),
#    Column('venue_id', Integer, ForeignKey('venue.venue_id'), nullable=False),
#    Column('approved', TINYINT, nullable=False)
#)
