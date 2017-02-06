from openshift.helper import KubernetesObjectHelper

project_helper = KubernetesObjectHelper('v1', 'project')
print(project_helper.get_object('test'))
project_helper.delete_object('test')
print(project_helper.get_object('test'))



service_helper = KubernetesObjectHelper('v1', 'service')
print(service_helper.get_object('test', 'test'))
