import yaml
import configs
from jinja2 import Template
import json
import sys

def removeTrailingComma(str):
    if str.startswith(','):
        str = str[1:]
    if str.endswith(','):
        str = str[:-1]
    return str
def getInstanceList(env_file, env_name):
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
    try:
        for env_elem in yaml.load(open(env_file)):
            if env_elem['name'] == env:
                return env_elem['heat_stack_name']
    except Exception as e:
        return e

def getEnvironmentList(env_file):
    env_list = []
    try:
        for env in yaml.load(open(env_file)):
            env_list.append(env['name'])
        return env_list
    except Exception as e:
        return e

def getInstanceDetails(env_file, env, inst_list):
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
    net_det = []
    try:
        for env_elem in yaml.load(open(env_file)):
            if env_elem['name'] == env:
                return env_elem['networks']
    except Exception as e:
        return e

def getSecurityGroupDetails(env_file, env):
    secgp_det = []
    try:
        for env_elem in yaml.load(open(env_file)):
            if env_elem['name'] == env:
                return env_elem['security_groups']
    except Exception as e:
        return e

def processJinja(jinja_template, datavars):
    try:
        HOTemplate = Template(open(jinja_template).read())
        output = HOTemplate.render(datavars)
        return output
    except Exception as e:
        return e
def dateHandler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
def yamltojson(yaml_template):
    return json.dumps(yaml.load(yaml_template), sys.stdout, default = dateHandler)
def replaceQuotes(obj):
    return obj.replace("\"", "\\\"")


