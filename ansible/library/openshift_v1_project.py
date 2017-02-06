#!/usr/bin/python

from __future__ import print_function

from openshift.ansible import OpenShiftAnsibleModule, OpenShiftAnsibleModuleError
from ansible.module_utils.basic import BOOLEANS


def main():
    try:
        module = OpenShiftAnsibleModule('project', 'V1')
        module.execute_module()
    except OpenShiftAnsibleModuleError as e:
        print(e)
        raise SystemExit(1)

if __name__ == '__main__':
    main()
