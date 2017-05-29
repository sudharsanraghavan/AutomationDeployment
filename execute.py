import configs
import create_stacks
import sys
import getopt
import utils

env_file = 'env_instances.yml'
stack_template = 'HOT_LaunchStack.j2'
stack_params = 'HOT_Params.j2'

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hlte:i:", ["help", "launch", "terminate", "environment=", "instances="])
    except getopt.GetoptError as err:
        print str(err)
        print "Execute 'python execute -h' or 'python execute --help' for help"
        help()
        sys.exit()
    env_list = []
    inst_list = []
    for o, a in opts:
        if o in ("-h", "--help"):
            help()
            sys.exit()
        elif o in ("-l", "--launch"):
            launch(env_list, inst_list)
        elif o in ("-t", "--terminate"):
            terminate(env_list, inst_list)
        elif o in ("-e", "--environment"):
            env_list.append(a)
        elif o in ("-i", "--instances"):
            inst_list.append(a)
        else:
            assert False, "unhandled option"

def help():
    print "usage: 'python execute.py -e <env_name> -i <inst_list> -l' to launch the instances"
    print "usage: 'python execute.py -e <env_name> -i <inst_list> -t' to terminate the instances"
    print "-l : To launch the instances"
    print "-t : To Terminate the instances "
    print "-e : Environment name as mentioned in the config file"
    print "-i : Instances list. one or more instance shall be provided seperated by ',' or 'all' if all the provided instances to be launched"
    print "Usage Example -"
    env_name = utils.getEnvironmentList(env_file = env_file)[0]
    inst_list = utils.getInstanceList(env_file = env_file, env_name = env_name)
    print "python execute.py -e {0} -i all -l".format(env_name)
    print "python execute.py -e {0} -i {1} -l".format(env_name, inst_list)
    print "python execute.py -e {0} -i all -t".format(env_name)
    print "python execute.py -e {0} -i {1} -t".format(env_name, inst_list)
    print "(OR)"
    print "In case of multiple environments to be launched - Usage Example -"
    print "python execute.py -e <env_name1> -i <inst_list> -e <env_name2> -i <inst_list> -l"
    print "python execute.py -e <env_name1> -i <inst_list> -e <env_name2> -i <inst_list> -t"

def launch(env_list, inst_list):
    os_details = []
    for env, inst in zip(env_list, inst_list):
        if inst in 'all':
            inst = utils.getInstanceList(env_file = env_file, env_name = env)
        else:
            pass
        env_details = {
            'env': env,
            'env_file': env_file,
            'HOT_file': stack_template,
            'HOP_file': stack_params,
            'endpoint': create_stacks.CreateStacks(env),
            'inst_list': inst
        }
        os_details.append(env_details)
    return createstacks(os_details)

def createstacks(osdetails):
    for env in osdetails:
        env['endpoint'].generatevars(env)
        env['endpoint'].generateHOT()
        env['endpoint'].generateParams()
        env['endpoint'].launchStacks()
        env['endpoint'].getStackStatus()
def terminate(env_list, inst_list):
    print "Terminating environment {0} and instance {1}".format(env_list, inst_list)

if __name__ == "__main__":
    main(sys.argv[1:])