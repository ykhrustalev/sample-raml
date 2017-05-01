from urllib.parse import urlencode

import pytest
import requests

from app.models import Artist, Album, db


@pytest.fixture
def artist():
    yield Artist("a")


def test_post(server, artist):
    with server.app_context():
        db.session.add(artist)
        db.session.commit()
        artist_id = artist.id

    with server.app_context():
        assert Album.query.count() == 0

        data = {
            "isrc": 'ab-1AB-12-12345',
            "artist_id": artist_id,
            "name": "a",
            "label": "label",
            "year": 2010,
        }
        r = requests.post(server.url + "/albums", data=data)

        assert r.status_code == 200
        response_data = r.json()
        assert response_data['isrc'] == data['isrc']
        assert response_data['artist']['id'] == data['artist_id']
        assert response_data['name'] == data['name']
        assert response_data['label'] == data['label']
        assert response_data['year'] == data['year']

    with server.app_context():
        assert Album.query.count() == 1
        album = Album.query.first()
        assert album.isrc == data['isrc']
        assert album.artist_id == data['artist_id']
        assert album.name == data['name']
        assert album.label == data['label']
        assert album.year == data['year']


@pytest.mark.parametrize('data, field', [
    ({"isrc": ""}, "isrc"),
    ({"isrc": "ab-1AB-12-12345"}, "name"),
    ({"isrc": "ab-1AB-12-12345", "name": ""}, "name"),
    ({"isrc": "", "name": ""}, "isrc"),
])
def test_post_errors(server, artist, data, field):
    with server.app_context():
        db.session.add(artist)
        db.session.commit()
        artist_id = artist.id

    with server.app_context():
        assert Album.query.count() == 0

        data.update({"artist_id": artist_id})
        r = requests.post(server.url + "/albums", data=data)

        assert r.status_code == 422
        assert field in r.json()['message']
        assert Album.query.count() == 0


def test_post_errors_on_unique_isrc(server, artist):
    with server.app_context():
        db.session.add(artist)
        db.session.commit()
        artist_id = artist.id

    with server.app_context():
        album = Album('ab-1AB-12-12345', 'a', artist)
        db.session.add(album)
        db.session.commit()

        assert Album.query.count() == 1

        r = requests.post(server.url + "/albums", data={
            "isrc": 'ab-1AB-12-12345',
            "name": "b",
            "artist_id": artist_id,
        })

        assert r.status_code == 422
        assert 'isrc' in r.json()['message']
        assert Artist.query.count() == 1


def test_put(server, artist):
    with server.app_context():
        db.session.add(artist)
        artist2 = Artist("b")
        db.session.add(artist2)
        db.session.commit()
        album = Album('ab-1AB-12-12345', 'a', artist)
        db.session.add(album)
        db.session.commit()
        artist_id2 = artist2.id
        album_id = album.id

        assert Album.query.count() == 1

    data = {
        "isrc": 'ab-1AB-12-12346',
        "artist_id": artist_id2,
        "name": "b",
        "label": "label2",
        "year": 2011,
    }

    r = requests.put(server.url + "/album/{}".format(album_id), data=data)
    assert r.status_code == 200
    response_data = r.json()
    assert response_data['isrc'] == data['isrc']
    assert response_data['artist']['id'] == data['artist_id']
    assert response_data['name'] == data['name']
    assert response_data['label'] == data['label']
    assert response_data['year'] == data['year']

    with server.app_context():
        assert Album.query.count() == 1
        album = Album.query.first()
        assert album.isrc == data['isrc']
        assert album.artist_id == data['artist_id']
        assert album.name == data['name']
        assert album.label == data['label']
        assert album.year == data['year']


def test_put_same_isrc(server, artist):
    with server.app_context():
        db.session.add(artist)
        album = Album('ab-1AB-12-12345', 'a', artist)
        db.session.add(album)
        db.session.commit()
        album_id = album.id

        assert Album.query.count() == 1

        data = {"isrc": 'ab-1AB-12-12345'}
        r = requests.put(server.url + "/album/{}".format(album_id), data=data)
        assert r.status_code == 200
        assert r.json()['isrc'] == data['isrc']

    with server.app_context():
        assert Album.query.count() == 1
        album = Album.query.get(album_id)
        assert album.isrc == data['isrc']


@pytest.mark.parametrize('data, field', [
    ({"isrc": ""}, "isrc"),
    ({"isrc": "xxx"}, "isrc"),
    ({"name": ""}, "name"),
    ({"year": "ab"}, "year"),
    ({"year": 1899}, "year"),
    ({"year": 3001}, "year"),
    ({"label": ""}, "label"),
    ({"artist_id": 99999}, "artist"),
])
def test_put_errors(server, artist, data, field):
    with server.app_context():
        db.session.add(artist)
        album = Album('ab-1AB-12-12345', 'a', artist)
        db.session.add(album)
        db.session.commit()
        album_id = album.id

    with server.app_context():
        assert Album.query.count() == 1

        r = requests.put(server.url + "/album/{}".format(album_id), data=data)

        assert r.status_code == 422
        assert field in r.json()['message']
        assert Album.query.count() == 1


def test_delete(server, artist):
    with server.app_context():
        album = Album('ab-1AB-12-12345', 'a', artist)
        db.session.add(album)
        db.session.commit()

        assert Album.query.count() == 1

        r = requests.delete(server.url + "/album/{}".format(artist.id))
        assert r.status_code == 204

    with server.app_context():
        assert Album.query.count() == 0


def test_get_one(server, artist):
    with server.app_context():
        album = Album('ab-1AB-12-12345', 'a', artist)
        db.session.add(album)
        db.session.commit()

        assert Album.query.count() == 1

        r = requests.get(server.url + "/album/{}".format(artist.id))
        assert r.status_code == 200
        assert r.json()['name'] == artist.name


@pytest.mark.parametrize('arguments, names', [
    ({}, ["a", "b", "c"]),
    ({"page": 1, "per_page": 2}, ["a", "b"]),
    ({"page": 2, "per_page": 2}, ["c"]),
])
def test_get_many(server, artist, arguments, names):
    with server.app_context():
        db.session.add(Album('ab-1AB-12-12345', 'a', artist))
        db.session.add(Album('ab-1AB-12-12346', 'b', artist))
        db.session.add(Album('ab-1AB-12-12347', 'c', artist))
        db.session.commit()

    r = requests.get(server.url + "/albums?{}".format(urlencode(arguments)))
    assert r.status_code == 200
    items = r.json()
    assert len(items) == len(names)
    assert list(map(lambda x: x["name"], items)) == names
