#!/usr/bin/python3
"""Get todos

EP:
    GET /todos/{todo_id}

Author: Amol More
"""
import sys
from os.path import abspath, dirname, join

if not abspath(join(dirname(__file__), '../../../../')) in sys.path:
    sys.path.insert(0, abspath(join(dirname(__file__), '../../../../')))

from lib.common.reportlib import print_pretty
from lib.modules.rest import modules
from objects.rest.todos.todos_object import Todos
from testcases.rest.rest_constants import fancode_url

# constant
todo_id = 3

if __name__ == "__main__":

    # todos api
    todos_api = Todos(fancode_url)
    data = modules.get_todo(todos_api, todo_id)
    print_pretty(data)
    