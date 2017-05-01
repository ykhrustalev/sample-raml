import re

from marshmallow import (
    fields, ValidationError, Schema, post_load, validates_schema
)
from marshmallow_sqlalchemy import ModelSchema

from .models import Artist, Album


def validate_page(value):
    if value < 1:
        raise ValidationError('Should be positive integer.')


def validate_per_page(value):
    if not (0 < value <= 10):
        raise ValidationError('Should be in rage [1, 10].')


class PaginatorSchema(Schema):
    page = fields.Integer(default=1, validate=validate_page)
    per_page = fields.Integer(default=10, validate=validate_per_page)

    @post_load
    def make_object(self, in_data):
        for name, field in self.fields.items():
            if name not in in_data:
                in_data[name] = field.default
        return in_data


def name_must_not_be_blank(value):
    return must_not_be_blank("name")(value)


def must_not_be_blank(key):
    def f(value):
        if not value or value.strip == "":
            raise ValidationError("Should not be empty.", key)

    return f


def name_must_be_unique(value):
    if Artist.query.filter_by(name=value).count() > 0:
        raise ValidationError("Should be unique.", "name")


class ArtistSchema(ModelSchema):
    name = fields.Str(required=True, validate=name_must_not_be_blank)

    class Meta:
        fields = ("id", "name",)
        model = Artist

    @validates_schema
    def validate_instance(self, data):
        if (not self.instance or
                (self.instance
                 and 'name' in data
                 and self.instance.name != data['name'])):
            name_must_be_unique(data.get('name'))


def isrc_must_be_unique(value):
    if Album.query.filter_by(isrc=value).count() > 0:
        raise ValidationError("Should be unique.", "isrc")


def isrc_must_be_valid(value):
    m = re.match(r'^[a-zA-Z]{2}-[0-9a-zA-Z]{3}-\d{2}-\d{5}$', value)
    if not m:
        raise ValidationError("Should be valid ISRC code.", "isrc")


def year_must_be_valid(value):
    if not (1900 <= value <= 3000):
        raise ValidationError("Should be valid ISRC code.", "year")


def artist_should_exist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    if not artist:
        raise ValidationError("Should be existing artist.", "artist")
    return artist


class AlbumSchema(ModelSchema):
    isrc = fields.Str(required=True, validate=isrc_must_be_valid)
    name = fields.Str(required=True, validate=name_must_not_be_blank)
    label = fields.Str(validate=must_not_be_blank("label"))
    year = fields.Integer(validate=year_must_be_valid)
    artist = fields.Nested(ArtistSchema, only=('id', 'name'))

    class Meta:
        fields = ("id", "isrc", "name", "artist", "label", "year")
        model = Album

    @validates_schema(pass_original=True)
    def validate_instance(self, data, original_data):
        if 'artist_id' in original_data or not self.instance:
            artist = artist_should_exist(original_data.get('artist_id'))
            data['artist'] = artist

        if (not self.instance or
                (self.instance
                 and 'isrc' in data
                 and self.instance.isrc != data['isrc'])):
            isrc_must_be_unique(data.get('isrc'))


paginator_schema = PaginatorSchema()
artist_schema = ArtistSchema()
album_schema = AlbumSchema()
