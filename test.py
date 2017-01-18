from __future__ import print_function

import re
import string
import sys

import yaml

from kubernetes import config
#from kubernetes.config.exception import ConfigException
#from kubernetes import client as k8s_client
#from openshift import client

from openshift.ansible import AnsibleModule, AnsibleModuleException

def main():
#    config.load_kube_config()

    try:
        ansible_module = AnsibleModule(context='myproject/10-0-0-51:8443/system:admin')
    except AnsibleModuleException as e:
        print(e)
        sys.exit(1)

    types = ansible_module.types
    for t in types:
        for v in types[t]['versions']:
            for key in ('namespaced', 'all_namespaces', 'unnamespaced'):
                unique_operations = set([x['type'] for x in types[t][v]['methods'].get(key, {}) if 'type' in x])
                if len(unique_operations) != len(types[t][v]['methods'].get(key, {})):
                    print("Duplicate ops found for type: {}, version: {}, object: \n{}\n\n".format(t, v, yaml.dump(types[t])))

                unique_apis = set([x['api'] for x in types[t][v]['methods'].get(key, {}) if 'api' in x])
                if len(unique_apis) > 1:
                    print("Multiple apis for type: {}, version: {}, object: \n{}\n\n".format(t, v, yaml.dump(types[t])))

    for obj in ('Pod', 'Deployment', 'DeploymentConfig', 'BuildConfig', 'StatefulSet', 'Job'):
        print("looking for object: {}".format(obj))
        print(yaml.dump(types[obj]))


if __name__ == '__main__':
    main()
