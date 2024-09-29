#!/usr/bin/python3
"""
..module:: User object

Defines wrappers over user related REST API
"""
import sys
from os.path import abspath, dirname, join

if not abspath(join(dirname(__file__), '../../')) in sys.path:
    sys.path.insert(0, abspath(join(dirname(__file__), '../../')))

from lib.executors.restapilib import RestAPICall
from lib.common.reportlib import status_code_err, print_err, print_debug, \
    print_pretty, count_err, get_err
from lib.common.utilitylib import compare_dicts

class Users():
    """Users API
    """

    def __init__(self, url):
        """Create an instance of RESTful API Interface
        
        Args:
            url: The base URL of the API.
    
        """
        self.major_uri = '/users'
        self.api = RestAPICall(url)
    
    def _total_users(self):
        """Get total numbers of users."""
        try:
            response = self.list_users()[0]['json_data']
            return len(response)
        except Exception:
            print_err("Failed to get total users from list users API.")
            print_debug("API Response:")
            print_pretty(response)
            sys.exit(1)

    def list_users(self, params={}):
        """List users API
        EP:
            GET /users
        
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
    
    def get_user(self, user_id):
        """Get User

        EP:
            GET /users/{user_id}
        Args:
            user_id: id of user
        
        Returns:
            Tuple of response of paginated API, errors & boolean result of 
            operations
        """
        uri = f"{self.major_uri}/{user_id}"
        data = self.api.get(uri)

        if not data['status_code'] == 200:
            err = status_code_err()
            return (data, err, False)
        
        return (data, '', True)
    
    def create_user(self, payload, verify=True, verify_count=True):
        """Create user API
        
        EP:
            POST /users
        
        Args:
            payload: User dict
            verify: Verification flag
            verify_count: User count verification flag

        Returns:
            Tuple of response of paginated API, errors & boolean result of 
            operations
        """
        if verify_count:
            previous_count = self._total_users()
        
        data = self.api.post(self.major_uri, payload)

        if not data['status_code'] == 201:
            err = status_code_err()
            return (data, err, False)
        
        if verify_count:
            # Verify total count after creation of user
            new_count = self._total_users()
            if not new_count == previous_count + 1:
                err = count_err(new_count, previous_count + 1)
                return (data, err, False)
            
        if verify:
            # Verify successful get operation on user after creation
            user_id = data['json_data']['id']
            (response, err, result) = self.get_user(user_id)
            if not result:
                err = get_err('user', 'user_id', user_id)
                return (data, err, False)
            
            # compare and verify dictonaries in input payload and output data
            user_details = response['json_data']
            ignore_keys = []
            errors = compare_dicts(payload, user_details, 'User dict', \
                        'Response dict', ignore_keys)
            
            if errors:
                return (data, errors, False)
        
        return (data, '', True)
