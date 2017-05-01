from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Artist %r' % self.name


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    isrc = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    artist_id = db.Column(
        db.Integer, db.ForeignKey('artists.id'), nullable=False
    )
    artist = db.relationship(
        Artist, backref=db.backref('albums', lazy='dynamic')
    )
    label = db.Column(db.Text, nullable=True)
    year = db.Column(db.Integer, nullable=True)

    def __init__(self, isrc,  name, artist, label=None, year=None):
        self.isrc = isrc
        self.name = name
        self.artist = artist
        self.label = label
        self.year = year

    def __repr__(self):
        return 'Album %r' % self.name
