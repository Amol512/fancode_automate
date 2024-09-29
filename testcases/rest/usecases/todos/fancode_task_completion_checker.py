#!/usr/bin/python3
"""FanCode User Task Completion Checker.

EP:
    GET /users
    GET /todos

Author: Amol More
"""
import sys
from os.path import abspath, dirname, join

if not abspath(join(dirname(__file__), '../../../../')) in sys.path:
    sys.path.insert(0, abspath(join(dirname(__file__), '../../../../')))

from lib.common.reportlib import print_info, print_err, print_debug
from lib.modules.rest import modules, core_modules
from objects.rest.users.users_object import Users
from objects.rest.todos.todos_object import Todos
from testcases.rest.rest_constants import fancode_url

# constant
failed_users = list()
no_tasks_users = list()

if __name__ == "__main__":
    
    """Step 1. List users."""
    # users api
    users_api = Users(fancode_url)
    data = modules.list_users(users_api)
    
    """Step 2. Filter Fancode city users."""
    users_from_fancode_city = core_modules.users_from_fancode_city(data)
    
    """Step 3. Check Fancode city users have completed more than half of their 
    tasks"""
    # todos api
    todos_api = Todos(fancode_url)

    for user in users_from_fancode_city:
        percentage = core_modules.calculate_user_task_completion_percentage(
            todos_api, user['id'])

        """Step 4. Save list of users who have no tasks."""
        if percentage is None:
            no_tasks_users.append((user.get('id'), user.get('name', None)))
            # Skip to the next user if there are no tasks
            continue

        """Step 5. Save list of users who have not completed 50% of their 
        tasks."""
        if percentage < 50:
            failed_users.append((user.get('id'), user.get('name', None)))
    
    """Step 6. Report results."""
    if failed_users or no_tasks_users:
        if failed_users:
            print_err("The following users from FanCode city have not " \
                "completed more than half of their tasks:")
            print_debug(failed_users)
        if no_tasks_users:
            print_err("The following users from FanCode city have no tasks " \
                "assigned.")
            print_debug(no_tasks_users)
        sys.exit(1)

    print_info("All the users from FanCode city have completed more than " \
            "half of their tasks.")
