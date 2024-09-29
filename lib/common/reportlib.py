#!/usr/bin/python3
"""
..module:: reportlib

Reporting Library

This library includes all general and error reporting functions for objects and
testcases.
"""
import os
import json
import sys

# If DEBUG_FLAG is set to 1, the script will continue running despite the 
# error.
# If DEBUG_FLAG is set to 0, the script will exit with status code 1 to 
# indicate an error.
DEBUG_FLAG = int(os.getenv('DEBUG_FLAG', 1))

beautify_dict = {
    # Green
    'info': "\033[92m[INFO] %s\033[0m\n",
    # Red
    'error': "\033[31m[ERROR] %s\033[0m\n",
    # Cyan
    'debug': "\033[36m[DEBUG] %s\033[0m\n",
    # Yellow
    'warning': "\033[33m[WARNING] %s\033[0m\n",
    # Blue
    'curl': "\033[34m[cURL] %s\033[0m\n"
}

def print_wrapper(print_type, text):
    """Print text with its print tag

    Args:
        print_type: Type of info
        text: Text to be printed
    """
    if not text:
        text = ''
    else:
        text = beautify_dict[print_type] % text
    return text


def print_info(text, p=True):
    """Print text with [INFO] tag

    Args:
        text: Text to be printed
        p: Flag determining if text should be printed or returned
    """
    if p:
        print((print_wrapper('info', text)))
    else:
        return print_wrapper('info', text)


def print_err(text, p=True):
    """Print text with [ERROR] tag

    Args:
        text: Text to be printed
        p: Flag determining if text should be printed or returned
    """
    if p:
        print((print_wrapper('error', text)))
    else:
        return print_wrapper('error', text)


def print_debug(text, p=True):
    """Print text with [DEBUG] tag

    Args:
        text: Text to be printed
        p: Flag determining if text should be printed or returned
    """
    if p:
        print((print_wrapper('debug', text)))
    else:
        return print_wrapper('debug', text)


def print_warning(text, p=True):
    """Print text with [WARNING] tag

    Args:
        text: Text to be printed
        p: Flag determining if text should be printed or returned
    """
    if p:
        print((print_wrapper('warning', text)))
    else:
        return print_wrapper('warning', text)


def print_curl(text, p=True):
    """Print curl command with [cURL] tag

    Args:
        text: curl command to be printed
        p: Flag determining if text should be printed or returned
    """
    if p:
        print((print_wrapper('curl', text)))
    else:
        return print_wrapper('curl', text)


def print_pretty(data, p=True):
    """Print dictionary with proper indentation

    Args:
        data: Dictionary to be printed properly
        p: Flag determining if text should be printed or returned
    """
    if p:
        print((json.dumps(data, sort_keys=True, indent=4)))
    else:
        return json.dumps(data, sort_keys=True, indent=4)


def status_code_err():
    return print_err(
        "The API response did not match the expected status code.", p=False)


def module_report(data, err, result, obj, obj_type, op_type, should_pass=True, 
        message=None, fail_status_code=None):
    """Prints the module pass/fail report for every rest api operation.
    Common code for all modules.

    Args:
        data: Rest api result data
        err: Errors, if any
        result: Result flag (True/False)
        obj: Actual object value
        obj_type: Resource type on which operation is done
        op_type: Operation type (LIST. GET, CREATE, DELETE etc)
        should_pass: Flag indicating whether operation should pass or not
        message: If should_pass is False, we can verify error messages.
        fail_status_code: If should_pass is False, we can verify failed status 
            code.

    """

    try:
        print_curl(data['curl'])
    except KeyError:
        print_curl(data.get('command'))
    except Exception as e:
        pass

    if result:
        if should_pass:
            print_info(f"{op_type.title()} operation on {obj_type} [{obj}] " \
                    "was successful.")
        else:
            print_err(f"Unpreviliged {op_type} operation on {obj_type} " \
                    f"[{obj}] was successful.")
            if not DEBUG_FLAG:
                sys.exit(1)
    else:
        if should_pass:
            print_err(f"Failed to {op_type} {obj_type} [{obj}].")
            print(err)
            if not DEBUG_FLAG:
                sys.exit(1)

        else:
            print_info(f"Failed to {op_type} {obj_type} [{obj}] " \
                    "(Unprevileged operation).")

            try:
                # check for 500 status code
                if not fail_status_code == 500 and \
                    int(data['status_code']) == 500:
                    print_err(f"Failed to {op_type} {obj_type} [{obj}]" \
                            "with 500 status code.")
                    if not DEBUG_FLAG:
                        sys.exit(1)

                # check for failed status code
                if fail_status_code:
                    print_info(f"Verifying status code for {op_type} {obj_type}")
                    if not int(data['status_code']) == int(fail_status_code):
                        print_err("Failed to verify status code.")
                        print_debug(f"Actual code: [{data['status_code']}]")
                        print_debug(f"Expected code: [{fail_status_code}]")
                        if not DEBUG_FLAG:
                            sys.exit(1)

                    print_info(f"Status code [{fail_status_code}] verified.")
            except Exception:
                pass

            # should pass is FALSE, check for error message if not None
            if message:
                print_info(f"Verifying error message for {op_type} {obj_type}")

                # check object has an attribute with the given name
                if hasattr(data, 'response'):
                    err_message = data.response['Error']['Code']
                else:
                    err_message = data.get('json_data', {}).get('message') or \
                        data.get('json_data', {}).get('debugMessage') or  \
                        data.get('json_data', {}).get('statusMessage') or \
                        data.get('json_data', {}).get('codeDesc') or \
                        data.get('json_data', {}).get('errorMessage')

                # when err_message value is None, key error
                if not err_message:
                    print_err("No error message found.")
                    print_debug(data)
                    if not DEBUG_FLAG:
                        sys.exit(1)

                # if message is passed as list to check if err_message
                # matches from any of the message from list
                is_err_msg_matched = True
                if isinstance(message, list):
                    if err_message not in message:
                        is_err_msg_matched = False
                else:
                    if message not in err_message:
                        is_err_msg_matched = False
                if not is_err_msg_matched:
                    print_err("Error message is not correct. ")
                    print_debug(f"Actual message: [{err_message}]")
                    print_debug(f"Expected message: [{message}]")
                    if not DEBUG_FLAG:
                        sys.exit(1)

                print_info(f"Error message [{err_message}] verified.")


def count_err(new_count, expected_count):
    """Return count error
    
    Args:
        new_count: actual count of resource after API operation
        expected_count: expected count fo resource after API operation

    Returns:
        str: A formatted error message indicating that the count verification 
            failed, showing the expected and the actual counts.
    """
    return print_err(f"Count verification failed [expected: {expected_count},"\
                f" returned: {new_count}]", p=False)


def get_err(resource, resource_type, resource_value):
    """Returns error for GET operation on resource

    Args:
        resource: Type of resource
        resource_type: Type of search for resource
        resource_value: value of resource

    Returns:
        str: A formatted error message indicating the failure to query the 
            resource by the given search type and value.
    """

    return print_err(
        f"Failed to query {resource} by {resource_type} - {resource_value}",
        p=False)
