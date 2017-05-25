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
    for inst in yaml.load(open(env_file)):
        if inst['name'] == env_name:
            for eachinst in inst['instances']:
                inst_list = inst_list + "," + eachinst['name']
    return removeTrailingComma(inst_list)

def getEnvironmentList(env_file):
    env_list = []
    for env in yaml.load(open(env_file)):
        env_list.append(env['name'])
    return env_list

def getInstanceDetails(env_file, env, inst_list):
    instance_det = []
    for env_elem in yaml.load(open(env_file)):
        if env_elem['name'] == env:
            for inst_elem in inst_list.split(','):
                for inst in env_elem['instances']:
                    if inst_elem == inst['name']:
                        instance_det.append(inst)
    return instance_det
def getNetworkDetails(env_file, env):
    net_det = []
    for env_elem in yaml.load(open(env_file)):
        if env_elem['name'] == env:
            return env_elem['networks']

def getSecurityGroupDetails(env_file, env):
    secgp_det = []
    for env_elem in yaml.load(open(env_file)):
        if env_elem['name'] == env:
            return env_elem['security_groups']

def processJinja(jinja_template, datavars):
    HOTemplate = Template(open(jinja_template).read())
    output = HOTemplate.render(datavars)
    return output
def dateHandler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
def yamltojson(yaml_template):
    return json.dumps(yaml.load(yaml_template), sys.stdout, default = dateHandler)
def replaceQuotes(obj):
    return obj.replace("\"", "\\\"")


