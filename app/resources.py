from flask import request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest, UnprocessableEntity

from .models import Artist, Album, db
from .schemas import paginator_schema, artist_schema, album_schema


def get_paginator():
    paginator, errors = paginator_schema.load(request.args)
    if errors:
        raise BadRequest(errors)
    return paginator


class ArtistListResource(Resource):
    def get(self):
        paginator = get_paginator()

        articles = Artist.query.order_by('id').paginate(
            page=paginator['page'],
            per_page=paginator['per_page'],
            error_out=False
        ).items

        return artist_schema.dump(articles, many=True).data

    def post(self):
        artist, errors = artist_schema.load(request.form, session=db.session)
        if errors:
            raise UnprocessableEntity(errors)

        db.session.add(artist)
        db.session.commit()

        return artist_schema.dump(artist).data


class ArtistResource(Resource):
    def get(self, artist_id):
        artist = Artist.query.get_or_404(artist_id)
        return artist_schema.dump(artist).data

    def put(self, artist_id):
        artist = Artist.query.get_or_404(artist_id)
        artist, errors = artist_schema.load(
            request.form,
            partial=True,
            instance=artist,
            session=db.session
        )
        if errors:
            raise UnprocessableEntity(errors)

        db.session.add(artist)
        db.session.commit()

        return artist_schema.dump(artist).data

    def delete(self, artist_id):
        artist = Artist.query.get_or_404(artist_id)

        Album.query.filter_by(artist_id=artist_id).delete()
        db.session.delete(artist)
        db.session.commit()

        return {}, 204


class AlbumListResource(Resource):
    def get(self):
        paginator = get_paginator()

        articles = Album.query.order_by('id').paginate(
            page=paginator['page'],
            per_page=paginator['per_page'],
            error_out=False
        ).items

        return album_schema.dump(articles, many=True).data

    def post(self):
        album, errors = album_schema.load(request.form, session=db.session)
        if errors:
            raise UnprocessableEntity(errors)

        db.session.add(album)
        db.session.commit()

        return album_schema.dump(album).data


class AlbumResource(Resource):
    def get(self, album_id):
        album = Album.query.get_or_404(album_id)
        return album_schema.dump(album).data

    def put(self, album_id):
        album = Album.query.get_or_404(album_id)
        album, errors = album_schema.load(
            request.form,
            partial=True,
            instance=album,
            session=db.session
        )
        if errors:
            raise UnprocessableEntity(errors)

        db.session.add(album)
        db.session.commit()

        return album_schema.dump(album).data

    def delete(self, album_id):
        album = Album.query.get_or_404(album_id)
        db.session.delete(album)
        db.session.commit()

        return {}, 204


def routes(app):
    api = Api(app)

    api.add_resource(ArtistListResource, '/artists')
    api.add_resource(ArtistResource, '/artist/<int:artist_id>')

    api.add_resource(AlbumListResource, '/albums')
    api.add_resource(AlbumResource, '/album/<int:album_id>')
