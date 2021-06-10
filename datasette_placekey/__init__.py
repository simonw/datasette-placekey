import json

import placekey
from datasette import hookimpl


@hookimpl
def prepare_connection(conn):
    conn.create_function(
        "geo_to_placekey",
        2,
        lambda lat, long: placekey.geo_to_placekey(float(lat), float(long)),
    )
    conn.create_function(
        "placekey_to_geo", 1, lambda pk: repr(list(placekey.placekey_to_geo(pk)))
    )
    conn.create_function(
        "placekey_to_geo_latitude", 1, lambda pk: placekey.placekey_to_geo(pk)[0]
    )
    conn.create_function(
        "placekey_to_geo_longitude", 1, lambda pk: placekey.placekey_to_geo(pk)[1]
    )
    conn.create_function("placekey_to_h3", 1, placekey.placekey_to_h3)
    conn.create_function("h3_to_placekey", 1, placekey.h3_to_placekey)
    conn.create_function(
        "placekey_to_geojson",
        1,
        lambda pk: json.dumps(placekey.placekey_to_geojson(pk)),
    )
    conn.create_function("placekey_to_wkt", 1, placekey.placekey_to_wkt)
    conn.create_function(
        "placekey_format_is_valid", 1, placekey.placekey_format_is_valid
    )
