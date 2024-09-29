# fancode_automate

## Prerequisites

Before running this project, ensure you have the following installed on your 
machine:

- **Python 3.x**: [official Python website](https://www.python.org/downloads/).
- **Requests 2.x** [official Pypi website](https://pypi.org/project/requests/).

ARCHITECTURE
------------
            Test-cases
                |
        Page specific objects
                |
        Python Requests library

STRUCTURE
---------

Set one core library which will directly talk to Python's 'requests' module 
(HTTP for human). This library will do all the encoding and formating of data 
and hide all the HTTP complexity, giving clean interface to upper layer.

# FanCode User Task Completion Checker

This project automates the verification that all users from the city 
**FanCode** have completed more than half of their to-do tasks. The 
identification of users from **FanCode** is based on their geographical 
coordinates: latitude between **-40 and 5** and longitude between **5 and 100**.

## Project Structure

- **testcases/rest/usecases/todos/fancode_task_completion_checker.py**: Main 
script for checking task completion.
- **lib/modules/rest/core_modules.py**: Utility functions for calculating task 
completion and filtering users.
- **objects/rest/users/users_object.py**: User API interaction methods.
- **objects/rest/todos/todos_object.py**: To-Do API interaction methods.
- **lib/common/reportlib.py**: Reporting utilities for logging information, 
errors, and debug messages.

## Helper function from core_modules.py

1. **core_modules.users_from_fancode_city(data)**:
    Filters a list of users to return only those who belong to the city FanCode.

2. **core_modules.calculate_user_task_completion_percentage(users)**
    Calculates the percentage of completed to-do tasks for a given user.

## Workflow

1. **List Users**: Fetches all users using the Users API.
2. **Filter FanCode Users**: Filters users based on their geographical 
coordinates to include only those from **FanCode** city.
3. **Check Task Completion**: For each filtered user, retrieves their tasks and 
calculates the percentage of completed tasks.
4. **Report Results**:
   - Lists users who have not completed more than 50% of their tasks.
   - Lists users who have no tasks assigned.
   - If all users from **FanCode** have completed more than 50% of their tasks, 
   a success message is printed.

## How to Run

1. **Clone the Repository**:
   ```bash
   - git clone git@github.com:Amol512/fancode_automate.git
   - cd fancode_automate

2. **Install the Dependencies**:
    ```bash
    - pip install -r requirements.txt

3. **Execute the script**:
    ```bash
    - python3 testcases/rest/usecases/todos/fancode_task_completion_checker.py

## Automation Framework Breakdown

1. **Core Libraries**

```lib/executors/restapilib.py```
RESTful API Wrapper Interface
This is the core library that handles the HTTP interface using the requests 
module. It serves as the backbone for executing API requests and managing 
responses.

```lib/common/reportlib.py```
Reporting Library
This library includes functions for general and error reporting, which can be 
used in test cases and object validation.

```lib/common/utilitylib.py```
Utility Library
Contains various general-purpose utility functions that aid in different 
operations, such as data transformations, dictionary comparisons, and cURL 
command generation.

2. **REST Modules**

```lib/modules/rest/core_modules.py```
REST Data Manipulation and Filtering Utilities
This module houses utility functions that assist in handling and manipulating 
REST API data. It’s where you add functions for filtering, sorting, or 
transforming data received from APIs.

```lib/modules/rest/modules.py```
Common REST API Operation Wrappers
All common API operations are organized into sections here. Before adding new 
APIs, search within this module for existing implementations. Add new sections 
when introducing a new API type.

4. **Object layer**

```objects/rest/```
This module defines wrappers over REST APIs. It abstracts API operations to 
make a actions reusable and easier to integrate into test cases.

5. **Constants**

```testcases/rest/rest_constants.py```
REST API Constants
This file defines constants related to REST APIs, such as URL endpoints and 
HTTP status codes. These constants should be used across all modules and test 
cases for consistency.

6. **Test Cases and Use Cases**

```testcases/rest/testcases```
This folder contains unit and integration test cases for the APIs. The test 
cases are written to validate specific API functionality.

```testcases/rest/usecases```
This folder holds end-to-end use cases that simulate real-world API workflows 
and scenarios. These use cases combine multiple API operations to validate 
system-level behavior.
