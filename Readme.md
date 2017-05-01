# Run application

To run need to have docker-compose and docker (1.11+) installed

    make docker-run

Try some examples

    curl http://localhost:5000/artists -d"name=Someone"
    {
        "id": 1,
        "name": "Someone"
    }
    
    curl http://localhost:5000/artists
    [
        {
            "id": 1,
            "name": "Someone"
        }
    ]
    
    curl http://localhost:5000/albums -d"isrc=ab-bcd-12-34567&artist_id=1&name=new title&label=independant&year=1999" -X POST
    {
        "artist": {
            "id": 1,
            "name": "Someone"
        },
        "id": 1,
        "isrc": "ab-bcd-12-34567",
        "label": "independant",
        "name": "new title",
        "year": 1999
    }

    curl http://localhost:5000/album/1 -d"year=1999" -X POST
    {
        "artist": {
            "id": 1,
            "name": "Someone"
        },
        "id": 1,
        "isrc": "ab-bcd-12-34567",
        "label": "independant",
        "name": "new title",
        "year": 2000
    }



Application will be available on http://localhost:5000


# Running tests

1. setup virtualenv

    make env

2. start test db

    make test-db-start

3. run pytest

    make test


If you want to use own database for tests, specify `DATABASE_URI`

    make DATABASE_URI=postgres://localhost:5432/app test
