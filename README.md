# python-openshift

Currently requires https://github.com/kubernetes-incubator/client-python/pull/98 for the kubernetes library to support update

Token-based auth is not currently working, most likely needs to be updated for OpenShift oauth endpoint


Test modules are in ansible/library

To test modules, run tox -e py27-modules
