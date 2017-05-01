import pytest
from marshmallow import ValidationError

from app.schemas import isrc_must_be_valid
from app.schemas import paginator_schema


@pytest.mark.parametrize('input, output', [
    ({}, {"page": 1, "per_page": 10}),
    ({"page": 2}, {"page": 2, "per_page": 10}),
    ({"per_page": 3}, {"page": 1, "per_page": 3}),
    ({"page": 2, "per_page": 3}, {"page": 2, "per_page": 3}),
])
def test_paginator_schema(input, output):
    data, errors = paginator_schema.load(input)
    assert errors == {}
    assert data == output


@pytest.mark.parametrize('input', [
    'ab-1AB-12-12345',
    'AA-123-00-12345',
])
def test_valid_isrc(input):
    isrc_must_be_valid(input)


@pytest.mark.parametrize('input', [
    '00-1AB-12-12345',
    'aAA-123-00-12345',
])
def test_invalid_isrc(input):
    with pytest.raises(ValidationError):
        isrc_must_be_valid(input)
