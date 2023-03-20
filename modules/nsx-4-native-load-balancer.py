#!/usr/bin/env python
import requests
import yaml

class NSXAPI:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.headers = {'Content-Type': 'application/json'}
        self.session = requests.Session()
        self.login()

    def login(self):
        url = f"https://{self.host}/api/session/create"
        data = {"j_username": self.username, "j_password": self.password}
        response = self.session.post(url, headers=self.headers, json=data)
        response.raise_for_status()

    def logout(self):
        url = f"https://{self.host}/api/session/destroy"
        response = self.session.post(url, headers=self.headers)
        response.raise_for_status()

    def call_api(self, endpoint, method='GET', data=None):
        url = f"https://{self.host}/api/{endpoint}"
        response = self.session.request(method, url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    # Load Balancer API functions
    def list_load_balancers(self):
        endpoint = "loadbalancer/services"
        return self.call_api(endpoint)

    def get_load_balancer(self, lb_id):
        endpoint = f"loadbalancer/service/{lb_id}"
        return self.call_api(endpoint)

    def create_load_balancer(self, lb_config):
        endpoint = "loadbalancer/service"
        return self.call_api(endpoint, method='POST', data=lb_config)

    def update_load_balancer(self, lb_id, lb_config):
        endpoint = f"loadbalancer/service/{lb_id}"
        return self.call_api(endpoint, method='PUT', data=lb_config)

    def delete_load_balancer(self, lb_id):
        endpoint = f"loadbalancer/service/{lb_id}"
        return self.call_api(endpoint, method='DELETE')


# Parse the YAML file and extract the endpoints and parameters
with open("/usr/share/ansible/custom_modules/data/vmware_nsx_api_spec.yaml") as file:
    api_spec = yaml.load(file, Loader=yaml.FullLoader)

load_balancer_spec = api_spec['loadbalancer']['services']

create_lb_params = load_balancer_spec['create']['parameters']
update_lb_params = load_balancer_spec['update']['parameters']
delete_lb_params = load_balancer_spec['delete']['parameters']
get_lb_params = load_balancer_spec['get']['parameters']
list_lb_params = load_balancer_spec['list']['parameters']
