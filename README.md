# python-openshift

Currently requires https://github.com/kubernetes-incubator/client-python/pull/98 for the kubernetes library to support update

Currently test.py and test_unnamespaced.py contain a test script that can be modified for hacking
Example use is: 
```
echo '{"ANSIBLE_MODULE_ARGS": {"name": "test", "api_version": "v1"}}' | python test_unnamespaced.py
echo '{"ANSIBLE_MODULE_ARGS": {"name": "test", "namespace": "test", "api_version": "v1"}}' | python test.py
```
