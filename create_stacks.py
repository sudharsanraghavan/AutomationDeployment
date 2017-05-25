import configs
import getpass
import json
import requests
import sys
import utils

class CreateStacks(object):
    def __init__(self, env):
        self.env = env
        self.authtoken = self.AuthToken()
    def AuthToken(self):
        """ Authentication method to generate token based on the identity version """
        # Read the password from user
        ospasswd = getpass.getpass(prompt = "Environment [ " + self.env + " ] - Enter the password for user " + configs.os_environment[self.env]['user'] + ":")
        # v3 Token generation
        if configs.os_environment[self.env]['identity_version'] == 'v3':
            keystone_url = configs.os_environment[self.env]['host_url'] + ':5000/v3/auth/tokens'
            keystone_data = json.dumps({"auth": {"identity": {"methods": ["password"],"password": {"user": {"name": configs.os_environment[self.env]['user'],"domain": {"name": configs.os_environment[self.env]['domain_name']},"password": ospasswd}}},"scope": {"project": {"name": configs.os_environment[self.env]['project_name'],"domain": {"name": configs.os_environment[self.env]['domain_name']}}}}})
            keystone_header = {'Content-type': 'application/json', 'Accept': 'application/json'}
            try:
                keystone_resp = requests.post(url = keystone_url, data = keystone_data, headers = keystone_header)
                if keystone_resp.status_code != 201:
                    sys.exit("Keystone Authentication Failed: " + keystone_resp.json()['error']['message'])
                osToken = {}
                osToken['token'] = keystone_resp.headers['X-Subject-Token']
                osToken['os_version'] = configs.os_environment[self.env]['os_version']
                for component in keystone_resp.json()['token']['catalog']:
                    for endpoint in component['endpoints']:
                        if endpoint['interface'] == 'public':
                            osToken[component['name']] = endpoint['url']
                return osToken
            except Exception as e:
                return e
        # v2 Token generation
        else:
            pass
            # steps for v2 token generation

    def generatevars(self, env):
        self.templatevars = dict()
        self.templatevars.update(env['endpoint'].authtoken)
        self.templatevars['secgroup'] = env['security_groups']
        self.templatevars['networks'] = env['network_details']
        self.templatevars['instances'] = env['inst_details']
        return self.templatevars

    def generateHOT(self, env):
        self.hot = utils.yamltojson(utils.processJinja(jinja_template = env['HOTemplate'], datavars = self.templatevars))
        return self.hot

    def generateParams(self, env):
        self.hop = utils.yamltojson(utils.processJinja(jinja_template = env['HOTparams'], datavars = self.templatevars))
        self.files_hop = utils.replaceQuotes(self.hop)
        return self.hop, self.files_hop

    def launchStacks(self, env):
        heat_headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-Auth-Token': env['endpoint'].authtoken['token']}
        heat_data = '{"files": {"file:///params":\"' + self.files_hop + '\"},'
        heat_data += '"disable_rollback": true,'
        heat_data += '"parameters": {},'
        heat_data += '"stack_name": "launchstack",'
        heat_data += '"environment_files": ["file:///params"],'
        heat_data += '"environment": ' + self.hop + ','
        heat_data += '"template": ' + self.hot + '}'
        try:
            heat_response = requests.post(url = env['endpoint'].authtoken['heat'] + '/stacks', data=heat_data, headers=heat_headers)
            if heat_response.status_code != 201:
                sys.exit("HEAT Stack creation Failed: " + heat_response.json()['error']['message'])
            self.stack_id = heat_response.json()['stack']['id']
            self.stack_url = heat_response.json()['stack']['links'][0]['href']
            return self.stack_id, self.stack_url
        except Exception as e:
            return e


