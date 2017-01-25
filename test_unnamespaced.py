from __future__ import print_function

import re
import string
import sys

import yaml

from openshift.ansible import OpenShiftAnsibleModule, OpenShiftAnsibleModuleError

def main():
    try:
        for obj in ('Project', 'Namespace'):
            ansible_module = OpenShiftAnsibleModule(obj)

            print("argument spec for object: {}".format(obj))
            print(yaml.dump(ansible_module.argument_spec))
            ansible_module.execute_module()
    except OpenShiftAnsibleModuleError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
