#!/usr/bin/python3
"""
..module:: utilitylib

Utility library

This library contains general utility methods
"""

import json
import sys
from os.path import abspath, dirname, join

if not abspath(join(dirname(__file__), '../../')) in sys.path:
    sys.path.insert(0, abspath(join(dirname(__file__), '../../')))

from lib.common.reportlib import print_err

def generate_curl_cmd(response_dict):
    """Generate a curl command for REST API call

    Args:
        response_dict: response data of API call

    Returns:
        curl command of given REST API response
    """

    [method, url] = response_dict['url'].split(' ')

    # Basic curl command
    curl_cmd = "curl -v -k -X "

    # Header(s)
    header_cmd = ''
    try:
        for header, value in list(response_dict['input-headers'].items()):
            header_cmd += " -H '%s: %s'" % (header, value)
    except Exception:
        header_cmd = ''

    # Payload
    try:
        payload = response_dict['payload']

        if response_dict['input-headers']['Content-Type'] ==  'text/plain':
            payload = json.dumps(payload, encoding="utf8",
                                ensure_ascii=False).encode('utf8')
            payload_cmd = " -d $'%s' " % payload.strip('"')
        else:
            payload_cmd = " -d '%s' " % payload
    except KeyError:
        payload_cmd = ' '
    except Exception:
        payload_cmd = ' '
        payload = "(truncated data)"

    curl_cmd = curl_cmd + method + header_cmd + payload_cmd + url
    return curl_cmd


def compare_dicts(dict1, dict2, dict_1_name, dict_2_name, ignore_keys=[]):
    """Compares two dictionaries.

    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.
        dict_1_name (str): Name of the dict1
        dict_2_name (str): Name of the dict2
        ignore_keys (list): A list of keys to ignore during comparison.

    Returns:
        str or none: None if both dictionaries are equal, 
            Error messages string otherwise.
    """
    try:
        # Remove ignored keys from both dictionaries
        dict1_filtered = {key: value for key, value in dict1.items() if key \
                        not in ignore_keys}
        dict2_filtered = {key: value for key, value in dict2.items() if key \
                        not in ignore_keys}

        # Check if both dictionaries have the same keys
        if dict1_filtered.keys() != dict2_filtered.keys():
            key_err = "Keys missing in dictionaries. \n" \
                f"{dict_1_name}: {dict1_filtered.keys()}\n" \
                f"{dict_2_name}: {dict2_filtered.keys()}"
            return print_err(key_err, p=False)

        # Check if the values for each key are the same
        for key in dict1_filtered:
            if dict1_filtered[key] != dict2_filtered[key]:
                value_err = f"Mismatch at key '{key}',\n " \
                    f"{dict_1_name}: {dict1_filtered[key]},\n" \
                    f"{dict_2_name}: {dict2_filtered[key]}"
                return print_err(value_err, p=False)
        
        return None

    except Exception as err:
        return print_err(err, p=False)
