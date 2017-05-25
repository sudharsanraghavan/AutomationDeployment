import yaml
import configs
from jinja2 import Template
import json
import sys

def removeTrailingComma(str):
    """ remove trailing comma from the string """
    if str.startswith(','):
        str = str[1:]
    if str.endswith(','):
        str = str[:-1]
    return str
def getInstanceList(env_file, env_name):
    """ Get the instance list from instance environment file """
    inst_list = ''
    try:
        for env in yaml.load(open(env_file)):
            if env['name'] == env_name:
                for eachinst in env['instances']:
                    inst_list = inst_list + "," + eachinst['name']
        return removeTrailingComma(inst_list)
    except Exception as e:
        return e

def getStackName(env_file, env):
    """ Get the stack name provided the environment file for that environment """
    try:
        for env_elem in yaml.load(open(env_file)):
            if env_elem['name'] == env:
                return env_elem['heat_stack_name']
    except Exception as e:
        return e

def getEnvironmentList(env_file):
    """ Get the environment list from the env file """
    env_list = []
    try:
        for env in yaml.load(open(env_file)):
            env_list.append(env['name'])
        return env_list
    except Exception as e:
        return e

def getInstanceDetails(env_file, env, inst_list):
    """ Get the instance details Ex - flavor, image from the env file for each instance provided """
    instance_det = []
    try:
        for env_elem in yaml.load(open(env_file)):
            if env_elem['name'] == env:
                for inst_elem in inst_list.split(','):
                    for inst in env_elem['instances']:
                        if inst_elem == inst['name']:
                            instance_det.append(inst)
        return instance_det
    except Exception as e:
        return e
def getNetworkDetails(env_file, env):
    """ Get the network details provided in the env file for that environment """
    net_det = []
    try:
        for env_elem in yaml.load(open(env_file)):
            if env_elem['name'] == env:
                return env_elem['networks']
    except Exception as e:
        return e

def getSecurityGroupDetails(env_file, env):
    """ Get the security group list provided in the environment file for that environment """
    secgp_det = []
    try:
        for env_elem in yaml.load(open(env_file)):
            if env_elem['name'] == env:
                return env_elem['security_groups']
    except Exception as e:
        return e

def processJinja(jinja_template, datavars):
    """ process the jinja template and render the output required """
    try:
        HOTemplate = Template(open(jinja_template).read())
        output = HOTemplate.render(datavars)
        return output
    except Exception as e:
        return e
def dateHandler(obj):
    """ Date handler to handle the version provided in the HEAT template """
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
def yamltojson(yaml_template):
    """ Convers yaml to json format """
    return json.dumps(yaml.load(yaml_template), sys.stdout, default = dateHandler)
def replaceQuotes(obj):
    """ Replace quotes for string formation """
    return obj.replace("\"", "\\\"")


