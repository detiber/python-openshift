import json
import re
import string

from ansible.module_utils.basic import AnsibleModule

from kubernetes import config
from kubernetes.config.config_exception import ConfigException
from openshift import client


class OpenShiftAnsibleModuleError(Exception):
    """
    Raised when there is an error inside of an Ansible module.
    """

    def __init__(self, message, **kwargs):
        """
        Creates an instance of the AnsibleModuleError class.
        :param message: The friendly error message.
        :type message: basestring
        :param kwargs: All other keyword arguments.
        :type kwargs: dict
        """
        self.message = message
        self.value = kwargs
        self.value['message'] = message

    def __str__(self):
        """
        String representation of the instance.
        """
        return json.dumps(self.value)


class OpenShiftAnsibleModule(AnsibleModule):
    def __init__(self, openshift_type):
        self.openshift_types = self._init_types()

        if openshift_type not in self.openshift_types:
            raise OpenShiftAnsibleModuleError(
                "Unkown type {} specified.".format(openshift_type)
            )

        argument_spec = {
            'state': {'default': 'present', 'choices': ['present', 'absent']},
            'name': {'required': True}
        }

        import yaml
        print(yaml.dump(argument_spec))
        mutually_exclusive = None
        required_together = None
        required_one_of = None
        required_if = None
        AnsibleModule.__init__(self, argument_spec, supports_check_mode=True)

#    def __init__(self, **kwargs):
#        self._init_client_config(**kwargs)
#        self.check_mode = kwargs.pop('check_mode', None)
#
#
#    def _init_client_config(self, **kwargs):
#        kubeconfig = kwargs.pop('kubeconfig', None)
#        context = kwargs.pop('context', None)
#
#        try:
#            # attempt to load the client config from file
#            config.load_kube_config(config_file=kubeconfig, context=context)
#        except IOError as e:
#            # TODO: attempt to create client config from args
#            raise AnsibleModuleException(
#                "Cannot determine api endpoint, please specify kubeconfig",
#                error=str(e)
#            )
#        except ConfigException as e:
#            raise AnsibleModuleException(
#                "Error generating client configuration",
#                error=str(e)
#            )
#        self.config = config
#
    @staticmethod
    def _init_types():
        version_pattern = re.compile("V\d((alpha|beta)\d)?")
        models = [x for x in dir(client.models) if version_pattern.match(x)]

        types = {}
        for model in models:
            match = version_pattern.match(model)
            version = match.group(0)
            name = version_pattern.sub('', model)
            if name in types:
                types[name]['versions'].append(version)
            else:
                types[name] = {'versions': [version]}

            types[name][version] = {'model_class': getattr(client, model), 'methods': {}}

        apis = [x for x in dir(client.apis) if version_pattern.search(x)]
        apis.append('OapiApi')
        for api in apis:
            match = version_pattern.search(api)
            if match is not None:
                version = match.group(0)
                name = version_pattern.sub('', api)[:-3]
            else:
                version = 'V1'
                name = api[:-3]
            api_class = getattr(client, api)

            for attr in dir(api_class):
                if attr.endswith('with_http_info'):
                    continue
                if attr.endswith('status'):
                    continue

                method_pattern = re.compile("^(create|delete_collection|delete|list|replace|patch|read)(_namespaced)?_(.*)?")
                match = method_pattern.match(attr)
                if match is None:
                    continue

                method = match.group(1)
                namespaced = match.group(2) != None
                object_name = match.group(3)

                all_namespaces = False
                if attr.endswith('_for_all_namespaces'):
                    all_namespaces = True
                    object_name = object_name[:-19]

                object_name = string.capwords(object_name, '_').replace('_','')
                object_version = version

                # TODO: find a way to better handle these
                if object_name == 'EvictionEviction':
                    object_name = 'Eviction'
                    object_version = 'V1beta1'
                elif object_name in ['ScaleScale', 'PodLog', 'NamespaceFinalize', 'DeploymentsScale',
                                     'ReplicasetsScale', 'ReplicationcontrollersScale',
                                     'LocalResourceAccessReview', 'ResourceAccessReview',
                                     'BuildRequestClone', 'BuildRequestInstantiate',
                                     'DeploymentRollbackRollback', 'DeploymentConfigRollbackRollback',
                                     'DeploymentRequestInstantiate', 'BuildLogLog', 'BindingBinding',
                                     'CertificateSigningRequestApproval', 'ScheduledJob',
                                     'DeploymentLogLog', 'SecretListSecrets', 'BuildDetails', '']:
                    continue
                if namespaced:
                    key = 'namespaced'
                elif all_namespaces:
                    key = 'all_namespaces'
                else:
                    key = 'unnamespaced'

                try:
                    if key not in types[object_name][object_version]['methods']:
                        types[object_name][object_version]['methods'][key] = []
                except KeyError:
                    print("missing version key for object: {}, api: {}, method: {}".format(object_name, api, attr))

                method_info = {
                    'type': method,
                    'name': attr,
                    'api': api,
                    'api_class': api_class,
                }
                types[object_name][object_version]['methods'][key].append(method_info)
        return types


