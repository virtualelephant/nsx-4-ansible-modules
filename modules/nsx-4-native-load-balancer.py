#!/usr/bin/env python

import requests
import yaml

from ansible.module_utils.basic import AnsibleModule

# Load the NSX API specification YAML file
with open('/usr/share/ansible/custom_modules/data/vmware_nsx_api_spec.yaml', 'r') as f:
    api_spec = yaml.safe_load(f)

# Define the base URL for NSX API requests
base_url = 'https://{}/api/{}'.format('{host}', api_spec['version'])

# Define the HTTP headers for NSX API requests
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Define the NSX error codes to ignore
ignore_errors = [
    '400 Bad Request',
    '404 Not Found',
    '409 Conflict',
    '503 Service Unavailable'
]

def send_api_request(action, url, headers, data=None):
    """
    Sends an API request to NSX and returns the response.

    Args:
        action (str): The HTTP method for the API request.
        url (str): The URL for the API request.
        headers (dict): The HTTP headers for the API request.
        data (dict): The data to send with the API request (optional).

    Returns:
        dict: The response from the API request.
    """

    # Build the full URL for the API request
    full_url = base_url + url

    # Send the API request and capture the response
    response = requests.request(action, full_url, headers=headers, json=data, verify=False)

    # If the response code is not in the ignore_errors list, raise an exception
    if response.status_code not in ignore_errors:
        response.raise_for_status()

    # If the response code is in the ignore_errors list, return an empty dictionary
    return {}

def create_load_balancer(module, host, username, password, lb_config):
    """
    Creates a new load balancer service in NSX.

    Args:
        module (AnsibleModule): The AnsibleModule object.
        host (str): The NSX hostname or IP address.
        username (str): The NSX API username.
        password (str): The NSX API password.
        lb_config (dict): The configuration for the load balancer service.

    Returns:
        dict: The result of the API request.
    """

    # Build the API request URL
    url = api_spec['nsx']['loadbalancer']['services']['create_lb_service']['url']

    # Build the API request data
    data = {
        'display_name': lb_config['display_name'],
        'description': lb_config['description'],
        'enabled': lb_config['enabled'],
        'ip_protocol': lb_config['ip_protocol'],
        'protocol_port': lb_config['protocol_port'],
        'source': {
            'ip_address': lb_config['source']['ip_address'],
            'port': lb_config['source']['port']
        },
        'destination': {
            'ip_address': lb_config['destination']['ip_address'],
            'port': lb_config['destination']['port']
        },
        'persistence_profile': {
            'type': lb_config['persistence_profile']['type'],
            'cookie_name': lb_config['persistence_profile']['cookie_name'],
            'cookie_mode': lb_config['persistence_profile']['cookie_mode']
        }
    }

    # Send the API request
    result = send_api_request('POST', url, headers, data)

    return result

def read_load_balancer(module, host, username, password, service_id):
    """
    Reads the configuration of an existing load balancer service in NSX.

    Args:
        module (AnsibleModule): The AnsibleModule object.
        host (str): The NSX hostname or IP address.
        username (str): The NSX API username.
        password (str): The NSX API password.
        service_id (str): The ID of the load balancer service.

    Returns:
        dict: The result of the API request.
    """

    # Build the API request URL
    url = api_spec['nsx']['loadbalancer']['services']['get_lb_service']['url'].format(lb_service_id=service_id)

    # Send the API request
    result = send_api_request('GET', url, headers)

    return result

def delete_load_balancer(module, host, username, password, service_id):
    """
    Deletes an existing load balancer service in NSX.

    Args:
        module (AnsibleModule): The AnsibleModule object.
        host (str): The NSX hostname or IP address.
        username (str): The NSX API username.
        password (str): The NSX API password.
        service_id (str): The ID of the load balancer service.

    Returns:
        dict: The result of the API request.
    """

    # Build the API request URL
    url = api_spec['nsx']['loadbalancer']['services']['delete_lb_service']['url'].format(lb_service_id=service_id)

    # Send the API request
    result = send_api_request('DELETE', url, headers)

    return result

def list_lb_service(module, host, username, password):
    """
    Lists all the load balancer services in NSX.

    Args:
        module (AnsibleModule): The AnsibleModule object.
        host (str): The NSX hostname or IP address.
        username (str): The NSX API username.
        password (str): The NSX API password.

    Returns:
        dict: The result of the API request.
    """

    # Build the API request URL
    url = api_spec['nsx']['loadbalancer']['services']['list_lb_service']['url']

    # Send the API request
    result = send_api_request('GET', url, headers)

    return result
