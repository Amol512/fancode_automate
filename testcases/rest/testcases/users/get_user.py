#!/usr/bin/python3
"""Get user

EP:
    GET /users/{user_id}

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

# Constant
user_id = 2

if __name__ == "__main__":

    # users api
    users_api = Users(fancode_url)
    data = modules.get_user(users_api, user_id)
    print_pretty(data)
