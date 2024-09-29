#!/usr/bin/python3
"""Create a user

EP:
    POST /users

Author: Amol More
"""
import sys
from os.path import abspath, dirname, join

if not abspath(join(dirname(__file__), '../../../../')) in sys.path:
    sys.path.insert(0, abspath(join(dirname(__file__), '../../../../')))

from lib.common.reportlib import print_pretty
from lib.modules.rest import modules
from objects.rest.users.users_object import Users
from testcases.rest.rest_constants import fancode_url

if __name__ == "__main__":
    
    # users api
    users_api = Users(fancode_url)

    payload = {
        "name": "AMOL MORE",
        "username": "amol_more",
        "email": "amol@gmail.com",
        "address": {
            "street": "High street",
            "suite": "Apt. 556",
            "city": "Pune",
            "zipcode": "92998-3874",
            "geo": {
                "lat": "-78.3159",
                "lng": "109.1496"
            }
        },
        "phone": "91-16862381",
        "website": "hildegard.org",
        "company": {
            "name": "Romaguera-Crona",
            "catchPhrase": "Hi my name is amol",
            "bs": "harness real-time e-markets"
        }
    }
    # Since we're using a fake API for testing purposes, 
    # we cannot retrieve newly added records from their database. 
    # Therefore, we've set the verify_count and verify flags to False 
    # to bypass the verification process during the user creation.
    data = modules.create_user(users_api, payload, verify_count=False, \
                        verify=False)
    print_pretty(data)
