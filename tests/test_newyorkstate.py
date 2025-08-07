# coding: utf8

import geocoder

location = '65 Niagara Square, Buffalo, NY 14202'


def test_newyorkstate():
    g = geocoder.newyorkstate(location)
    assert g.ok
    osm_count, fields_count = g.debug()[0]
    assert osm_count >= 6
    assert fields_count >= 13

