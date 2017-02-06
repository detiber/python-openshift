#!/usr/bin/env python

from __future__ import print_function

from openshift.ansible import (
    OpenShiftAnsibleModule, OpenShiftAnsibleModuleError)


def main():
    try:
        module = OpenShiftAnsibleModule('Namespace', 'V1')
        module.execute_module()
    except OpenShiftAnsibleModuleError as e:
        print(e)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
