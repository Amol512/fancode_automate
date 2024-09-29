#!/usr/bin/python3
"""
..module:: This module serves as a collection of utility functions related to 
REST data manipulation and filtering.

"""
import sys
from os.path import abspath, dirname, join

if not abspath(join(dirname(__file__), '../../../')) in sys.path:
    sys.path.insert(0, abspath(join(dirname(__file__), '../../../')))

from lib.common.reportlib import print_info, print_err, print_debug

def users_from_fancode_city(users):
    """
    Filters list of users to return only those who belong to the city FanCode.
    
    A user is considered to be from 'FanCode' if their 
    latitude is between -40 and 5 and longitude is between 5 and 100.

    Args:
        users: A list of user dictionaries where each user contains 
            'lat' and 'lng' keys representing their geographical coordinates.
    
    Returns:
        List: A list of user dictionaries filtered to include only those from 
            the city 'FanCode'.
    """
    print_debug("Filtering FanCode users from the list...")
    result = list()
    for user in users:
        lat = user['address']['geo']['lat']
        lng = user['address']['geo']['lng']

        # Check if the user is in the specified latitude and longitude range
        if -40 <= float(lat) <= 5 and 5 <= float(lng) <= 100:
            result.append(user)

    return result


def calculate_user_task_completion_percentage(todos_api, user_id):
    """Calculates the percentage of completed todo tasks for a user.
    Args:
        todos_api: an instance of todo api
        user_id: id of the user for retrive todos

    Returns:
        percentage: The percentage of completed tasks as a float value. 
            Returns None if there are no tasks.
    """
    print_debug(f"Calculating completion percentage for user - {user_id}")
    # Get the total number of tasks for the user
    params = {
        'userId': user_id
    }
    total_tasks = todos_api._total_todos(params)
    print_info(f"Total tasks for user {user_id}: {total_tasks}")
    
    # Return None if the user has no tasks
    if not total_tasks:
        print_err(f"No tasks found for user {user_id}.")
        return None
    
    # Update parameters to filter only completed tasks
    params['completed'] = 'true'
    
    # Get the number of completed tasks for the user
    completed_tasks = todos_api._total_todos(params)
    print_info(f"Completed tasks for user {user_id}: {completed_tasks}")

    percentage = int((completed_tasks / total_tasks) * 100)
    print_info(f"Completion percentage for user {user_id}: {percentage:.2f}%")

    return percentage
