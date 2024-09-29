#!/usr/bin/python3
"""
..module:: Todos object

Defines wrappers over todos related REST API
"""
import sys
from os.path import abspath, dirname, join

if not abspath(join(dirname(__file__), '../../')) in sys.path:
    sys.path.insert(0, abspath(join(dirname(__file__), '../../')))

from lib.executors.restapilib import RestAPICall
from lib.common.reportlib import status_code_err, print_err, print_debug, \
    print_pretty

class Todos():
    """
    Todos API
    """

    def __init__(self, url):
        """Create an instance of RESTful API Interface
        
        Args:
            url: The base URL of the API.
    
        """
        self.major_uri = '/todos'
        self.api = RestAPICall(url)
    
    def _total_todos(self, params={}):
        """Get total numbers of todos."""
        try:
            response = self.list_todos(params)[0]['json_data']
            return len(response)
        except Exception:
            print_err("Failed to get total todos from list todos API.")
            print_debug("API Response:")
            print_pretty(response)
            sys.exit(1)

    def list_todos(self, params={}):
        """List Todos API
        EP:
            GET /todos

        Args:
            params: Pagination and filteration params

        Returns:
            Tuple of response of paginated API, errors & boolean result of 
            operations
        
        """
        data = self.api.get(self.major_uri, params=params)

        if not data['status_code'] == 200:
            err = status_code_err()
            return (data, err, False)
        
        return (data, '', True)
    
    def get_todo(self, todo_id):
        """Get Todo

        EP:
            GET /todos/{todo_id}
        Args:
            todo_id: id of todo
        
        Returns:
            Tuple of response of paginated API, errors & boolean result of 
            operations
        """
        uri = f"{self.major_uri}/{todo_id}"
        data = self.api.get(uri)

        if not data['status_code'] == 200:
            err = status_code_err()
            return (data, err, False)
        
        return (data, '', True)
