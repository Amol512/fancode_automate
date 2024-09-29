#!/usr/bin/python3
"""
..module:: restapilib

RESTful API wrapper interface

This is the core library to handle HTTP interface using requests module.
"""

import requests
import json
import sys
from os.path import abspath, dirname, join

if not abspath(join(dirname(__file__), '../../')) in sys.path:
    sys.path.insert(0, abspath(join(dirname(__file__), '../../')))

from lib.common.utilitylib import generate_curl_cmd

class RestAPICall(object):
    """RESTful API Wrapper class
    """
    
    def __init__(self, base_url, **kwargs):
        """Initialize RESTful api object
        
        Args:
            base_url: URL of RESTful server.
        """
        self.url = base_url
        self.headers = kwargs.get('headers', {})
        self.verify = kwargs.get('verify', False)
        self.api_timout = kwargs.get('api_timeout')
        self.caller = requests
    
    def _return_wrapped_up_data(self, method, response, headers={}, \
        payload=None, content_type=None):
        """Return a wrapper over thhe response of a requests

        Args:
            method: HTTP method.
            response: Response dict of the HTTP requests.
            headers: Response headers from the HTTP request.
            payload: Input payload
            content_type: Content-Type

        Returns:
            Wrapper dict over the response.
        """
        response_dict = {
            'url': ' '.join([method.upper(), response.url]),
            'status_code': response.status_code,
            'input-headers': headers,
            'headers': dict(response.headers),
            'cookies': self.caller.cookies if isinstance(self.caller, \
                requests.sessions.Session) else {}
        }
        if content_type:
            response_dict['input-headers'].\
                update({'Content-Type': content_type})
        if payload:
            response_dict.update({'payload': payload})
        
        try:
            json_data = response.json()
        except (ValueError, RuntimeError):
            # No JSON object could be decoded
            json_data = {}
            try:
                text_data = response.text
                response_dict.update({'text_data': text_data})
            except (ValueError, RuntimeError):
                pass

            try:
                if response.headers['Content-Type'] in \
                    ['application/octet-stream', \
                    'application/x-zip-compressed', 'application/gzip', \
                    'application/pdf', 'application/zip']:
                    binary_data = response.content
                    response_dict.update({'binary_data': binary_data})
            except (KeyError, RuntimeError):
                pass
        response_dict.update({'json_data': json_data})

        # Add curl command in data
        curl = generate_curl_cmd(response_dict)
        response_dict['curl'] = curl
        return response_dict
    
    def get(self, uri, params=None, headers=None, content_type=None, \
        timeout=None):
        """GET method
        
        Args:
            uri: URI to be appended the URL
            params: Query params to be sent with requests
            headers: Headers for the HTTP request
            content_type: defaults to none for a get request
            timeout: API timout
        
        Returns:
            Wrapper dict over the response of requests
        """

        url = self.url + uri
        timeout = self.api_timout if timeout is None else timeout
        headers = {} if headers is None else headers
        params = {} if params is None else params

        headers.update(self.headers)
        if content_type is not None:
            headers.update({'Content-Type': content_type})

        response = self.caller.get(url, headers=headers, verify=self.verify, \
            params=params, timeout=timeout)
        
        return self._return_wrapped_up_data('GET', response, headers, \
            content_type=content_type)

    def post(self, uri, payload=None, headers=None, params=None, \
             content_type='application/json', timeout=None):
        """POST method
        
        Args:
            uri: URI to be appended the URL
            payload: Payload to be sent with requests
            headers: Headers for the HTTP request
            params: Query params to be sent with requests
            content_type: defaults to none for a get request
            timeout: API timout
        
        Returns:
            Wrapper dict over the response of requests
        """
        url = self.url + uri
        timeout = self.api_timout if timeout is None else timeout
        headers = {} if headers is None else headers
        params = {} if params is None else params

        # Updating headers
        headers.update(self.headers)
        if content_type is not None:
            headers.update({'Content-Type': content_type})

            # For content type application/json payload must be in json format
            if isinstance(payload, (dict)):
                if content_type == 'application/json':
                    payload = json.dumps(payload)
        response = self.caller.post(url, headers=headers, verify=self.verify, \
            params=params, data=payload, timeout=timeout)
        
        return self._return_wrapped_up_data('POST', response, headers, \
            payload, content_type)
