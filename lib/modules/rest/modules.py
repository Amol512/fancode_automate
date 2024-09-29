#!/usr/bin/python3
"""
..module:: Wrappers around common REST API operations

All API's are seperated in following different sections.
Search them before adding anything, and add a new section for new API's.
"""
import sys
from os.path import abspath, dirname, join

if not abspath(join(dirname(__file__), '../../')) in sys.path:
    sys.path.insert(0, abspath(join(dirname(__file__), '../../')))

from lib.common.reportlib import module_report

#################################### USERS ####################################
def list_users(users_api, params={}, should_pass=True):
    """Get list of users"""
    (data, errors, result) = users_api.list_users(params)
    module_report(data, errors, result, params, 'Users', 'List', should_pass)

    if result:
        return data['json_data']

def get_user(users_api, user_id, should_pass=True, message=None):
    """Get user"""
    (data, errors, result) = users_api.get_user(user_id)
    module_report(data, errors, result, user_id, 'User', 'Get', should_pass, \
        message)

    if result:
        return data['json_data']

def create_user(users_api, payload, verify=True, verify_count=True, \
        should_pass=True, message=None):
    """Create user"""
    (data, errors, result) = users_api.create_user(payload, verify, \
                                            verify_count)
    module_report(data, errors, result, payload['username'], 'User', \
        'Create', should_pass, message)

    if result:
        return data['json_data']

#################################### TODOS ####################################
def list_todos(todos_api, params={}, should_pass=True):
    """Get list of todos"""
    (data, errors, result) = todos_api.list_todos(params)
    module_report(data, errors, result, params, 'Todos', 'List', should_pass)

    if result:
        return data['json_data']

def get_todo(todos_api, todo_id, should_pass=True, message=None):
    """Get todo"""
    (data, errors, result) = todos_api.get_todo(todo_id)
    module_report(data, errors, result, todo_id, 'Todo', 'Get', should_pass, \
        message)

    if result:
        return data['json_data']
