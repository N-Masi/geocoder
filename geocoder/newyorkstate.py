#!/usr/bin/python
# coding: utf8

from __future__ import absolute_import

import logging
import re

from geocoder.base import OneResult, MultipleResultsQuery

class NewYorkStateResult(OneResult):

    @property
    def lat(self):
        return self.raw.get('location', {}).get('y')

    @property
    def lng(self):
        return self.raw.get('location', {}).get('x')
    
    @property
    def address(self):
        return self.raw.get('address')

    @property
    def housenumber(self):
        expression = r'\d+'
        matches = re.findall(expression, self.address)
        if matches:
            return matches[0]
        
    @property
    def street(self):
        expression = r'^\d*\s*([A-Za-z ]+)(?=,)'
        matches = re.findall(expression, self.address)
        if matches:
            return matches[0]

    @property
    def city(self):
        expression = r',\s*([^,]+)\s*,'
        matches = re.findall(expression, self.address)
        if matches:
            return matches[0]

    @property
    def state(self):
        return 'NY'
    
    @property
    def postal(self):
        expression = r'\d{5}'
        matches = re.findall(expression, self.address)
        if matches:
            return matches[-1]

    @property
    def country(self):
        return 'USA'

    @property
    def address(self):
        return self.raw.get('address')

    @property
    def accuracy(self):
        return self.raw.get('score')
    
class NewYorkStateQuery(MultipleResultsQuery):
    """
    NYS ITS Geocoder REST Services
    =======================
    Geocoding is the use of technology and reference data to return a geographic coordinate when a street address is entered. Geocoding is used when lists of addresses need to be placed on a map, when an address is entered in an application to center a map or return information for that location, or any other time you have an address, and a geographic coordinate is needed. An address is entered either manually or by bulk input from a database or other source. The geocoder then compares the entered address to a set of reference data. The geocoder returns a coordinate pair and standardized address for each input address it can match. The NYS ITS Geospatial Services geocoder uses a series of combinations of reference data and configuration parameters to optimize both the likelihood of a match and the quality of the results. The reference data supporting the geocoder is stored in NENA GIS Data Model standard.

    API Reference
    -------------
    https://gisservices.its.ny.gov/arcgis/rest/services/Locators/Street_and_Address_Composite/GeocodeServer
    https://gis.ny.gov/system/files/documents/2022/07/geocoding-help-101.pdf
    https://gis.ny.gov/address-geocoder
    """
    provider = 'newyorkstate'
    method = 'geocode'

    _URL = 'https://gisservices.its.ny.gov/arcgis/rest/services/Locators/Street_and_Address_Composite/GeocodeServer/findAddressCandidates'
    _RESULT_CLASS = NewYorkStateResult
    _KEY_MANDATORY = False

    def _build_params(self, location, provider_key, **kwargs):
        return {
            'SingleLine': location,
            'f': 'json',
            'outSR': 4326,
            'maxLocations': kwargs.get('maxRows', 1)
        }

    def _adapt_results(self, json_response):
        return json_response.get('candidates', [])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    g = NewYorkStateQuery('65 Niagara Square, Buffalo, NY 14202')
    g.debug()
