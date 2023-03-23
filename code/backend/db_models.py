from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from backend import login_manager
from flask_login import UserMixin
from backend import db, login_manager, app
from sqlalchemy.orm import backref


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    # return User.query.filter_by(username)


user_paper_collections = db.Table('user_paper_collections',
     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
     db.Column('paper_id', db.Integer, db.ForeignKey('paper.id')))


paper_author_collections = db.Table('paper_author_collections',
     db.Column('paper_id', db.Integer, db.ForeignKey('paper.id')),
     db.Column('author_id', db.Integer, db.ForeignKey('author.id')))


paper_subject_collections = db.Table('paper_subject_collections',
     db.Column('paper_id', db.Integer, db.ForeignKey('paper.id')),
     db.Column('subject_id', db.Integer, db.ForeignKey('subject.id')))


# user_paper_tag_collections = db.Table('user_paper_tag_collections',
#      db.Column('paper_id', db.Integer, db.ForeignKey('paper.id')),
#      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
#      db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
#      )


paper_tag_collections = db.Table('paper_tag_collections',
     db.Column('paper_id', db.Integer, db.ForeignKey('paper.id')),
     db.Column('tag_id', db.Integer, db.ForeignKey('user_tag.id')),     
     )


# user_tag_collections = db.Table('user_tag_collections',
#      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), unique=True)
    image_file = db.Column(db.String(60), nullable=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
        
    # tags = db.relationship('Tag', secondary=user_tag_collections, backref='user', lazy="dynamic")
    papers = db.relationship('Paper', secondary=user_paper_collections, lazy="dynamic", backref=backref("user", lazy="dynamic"))

    def __repr__(self):
        return f"{id}, User('{self.username}'), '{self.image_file}'"


class Paper(db.Model):
    __tablename__ = "paper"
    id = db.Column(db.Integer, primary_key=True)
    arxiv_id = db.Column(db.String(100), unique=True)
    pdf_url = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(100))
    abstract = db.Column(db.String(500))
    year = db.Column(db.Integer)

    authors = db.relationship("Author", secondary=paper_author_collections, backref="paper", lazy="dynamic")
    subjects = db.relationship("Subject", secondary=paper_subject_collections, backref="paper", lazy="dynamic")
    # user_tags = db.relationship("User_Tag", secondary=paper_tag_collections, backref="paper", lazy="dynamic")
    user_tags = db.relationship("User_Tag", secondary=paper_tag_collections, lazy="dynamic", backref=backref("paper", lazy="dynamic"))
    
    def __repr__(self):
        return f"{self.arxiv_id}, {self.title}, {self.abstract}, {self.year}, {self.authors}, {self.subjects}"

    def to_dict(self):
        return {
            'url': self.pdf_url,
            'title': self.title,
            'abstract': self.abstract,
            'year': self.year,
            'authors': [author.authorname for author in self.authors.all()],
            'subjects': [subject.subjectname for subject in self.subjects.all()],
            'tags': [tag.tagname for tag in self.user_tags.all()],
        }


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    authorname = db.Column(db.String(200))
    # insitution = db.Column(db.String(20), nullable=True)


class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    subjectname = db.Column(db.String(50))

    def __repr__(self):
        return f"{self.subjectname}"


class User_Tag(db.Model):
    __tablename__ = "user_tag"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), 
                        db.ForeignKey('user.username')
                        )
    # url = db.Column(db.String(100), db.ForeignKey('paper.url'))
    tagname = db.Column(db.String(50))


class Arxiv_history(db.Model):
    __tablename__ = "arxiv_history"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), 
                        db.ForeignKey('user.username')
                        )
    url = db.Column(db.String(100))
    search_time = db.Column(db.DateTime)


with app.app_context():
    # db.drop_all()
    db.create_all()
