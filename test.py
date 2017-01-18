from __future__ import print_function

import re
import string
import sys

import yaml

from openshift.ansible import OpenShiftAnsibleModule, OpenShiftAnsibleModuleError

def main():
    try:
        ansible_module = OpenShiftAnsibleModule('Project')
    except OpenShiftAnsibleModuleError as e:
        print(e)
        sys.exit(1)

    types = ansible_module.openshift_types
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
