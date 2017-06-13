Automation Deployment using HEAT orchestration engine on Openstack Environment

Usage Example

ubuntu@ubuntu:~/AutomationDeployment$ python execute.py -h
usage: 'python execute.py -e <env_name> -i <inst_list> -l' to launch the instances
usage: 'python execute.py -e <env_name> -i <inst_list> -t' to terminate the instances
-l : To launch the instances
-t : To Terminate the instances
-e : Environment name as mentioned in the config file
-i : Instances list. one or more instance shall be provided seperated by ',' or 'all' if all the provided instances to be launched
Usage Example -
python execute.py -e env1 -i all -l
python execute.py -e env1 -i inst1,inst2 -l
python execute.py -e env1 -i all -t
python execute.py -e env1 -i inst1,inst2 -t
(OR)
In case of multiple environments to be launched - Usage Example -
python execute.py -e <env_name1> -i <inst_list> -e <env_name2> -i <inst_list> -l
python execute.py -e <env_name1> -i <inst_list> -e <env_name2> -i <inst_list> -t
