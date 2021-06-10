import json
import sqlite3

import pytest

from datasette_placekey import prepare_connection


@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    prepare_connection(conn)
    return conn


@pytest.mark.parametrize(
    "sql,expected",
    (
        ("geo_to_placekey(33.0896104,129.7900839)", "@6nh-nhh-kvf"),
        ("placekey_to_geo_latitude('@6nh-nhh-kvf')", pytest.approx(33.090062930797316)),
        (
            "placekey_to_geo_longitude('@6nh-nhh-kvf')",
            pytest.approx(129.79012287161294),
        ),
        ("placekey_to_h3('@6nh-nhh-kvf')", "8a30d94e4c87fff"),
        ("h3_to_placekey('8a30d94e4c87fff')", "@6nh-nhh-kvf"),
        ("placekey_format_is_valid('@6nh-nhh-kvf')", 1),
        ("placekey_format_is_valid('@6nh-nhh-kv')", 0),
    ),
)
def test_placekey(conn, sql, expected):
    result = conn.execute("select " + sql).fetchone()[0]
    assert expected == result


@pytest.mark.parametrize(
    "sql,expected",
    (
        (
            "placekey_to_geo('@6nh-nhh-kvf')",
            [pytest.approx(33.090062930797316), pytest.approx(129.79012287161294)],
        ),
        (
            "placekey_to_geojson('@6nh-nhh-kvf')",
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            pytest.approx(129.7895236455708),
                            pytest.approx(33.09039125030504),
                        ],
                        [
                            pytest.approx(129.78940092277236),
                            pytest.approx(33.08981691255207),
                        ],
                        [
                            pytest.approx(129.79000014788863),
                            pytest.approx(33.08948858933029),
                        ],
                        [
                            pytest.approx(129.7907220986247),
                            pytest.approx(33.0897346054397),
                        ],
                        [
                            pytest.approx(129.7908448236134),
                            pytest.approx(33.0903089445816),
                        ],
                        [
                            pytest.approx(129.7902455956758),
                            pytest.approx(33.09063726622521),
                        ],
                        [
                            pytest.approx(129.7895236455708),
                            pytest.approx(33.09039125030504),
                        ],
                    ]
                ],
            },
        ),
    ),
)
def test_placekey_json(conn, sql, expected):
    result = conn.execute("select " + sql).fetchone()[0]
    assert expected == json.loads(result)


def test_placekey_to_wkt(conn):
    result = conn.execute("select placekey_to_wkt('@6nh-nhh-kvf')").fetchone()[0]
    assert result.startswith("POLYGON ((")
