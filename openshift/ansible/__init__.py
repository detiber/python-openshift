import copy
import json
import re

import string_utils

from ansible.module_utils.basic import AnsibleModule

from kubernetes import config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.rest import ApiException
from openshift import client
from openshift.helper import KubernetesObjectHelper

#: Regex for finding versions
VERSION_RX = re.compile("V\d((alpha|beta)\d)?")


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
    def __init__(self, kind, api_version, namespaced=False):
        self.api_version = api_version
        self.kind = kind
        self.model = self.__get_model(api_version, kind)
        self.namespaced = namespaced
        self.helper = KubernetesObjectHelper(api_version, kind)

        argument_spec = {
            'state': {
                'default': 'present',
                'choices': ['present', 'absent']
            },
            'name': {
                'required': True
            },
            'kubeconfig': {},
            'context': {}
        }

        model_obj = self.model()
        self.properties = self.__properties_from_model_obj(model_obj)

        if 'metadata' not in list(self.properties.keys()):
            raise OpenShiftAnsibleModuleError(
                "Object {} does not contain metadata field".format(self.model)
            )

        for prop in list(self.properties.keys()):
            prop_class = self.properties[prop]
            prop_obj = prop_class()
            prop_props = self.__properties_from_model_obj(prop_obj)

            # Do not expose Status to argument spec
            if prop == 'status':
                continue

            # Filter metadata properties added to argument spec
            if prop == 'metadata':
                if not isinstance(prop_obj, client.V1ObjectMeta):
                    raise OpenShiftAnsibleModuleError(
                        "Unknown metadata type: {}".format(prop_class)
                    )
                argument_spec['labels'] = {'required': False, 'type': 'dict'}
                argument_spec['annotations'] = {
                    'required': False,
                    'type': 'dict'
                }
                if self.namespaced:
                    argument_spec['namespace'] = {'required': True}
            else:
                for sub_prop in list(prop_props.keys()):
                    sub_prop_class = prop_props[sub_prop]

                    argument_spec[prop + '_' + sub_prop] = {
                        'required': False,
                        'type': sub_prop_class.__name__
                    }

        # mutually_exclusive = None
        # required_together = None
        # required_one_of = None
        # required_if = None
        AnsibleModule.__init__(self, argument_spec, supports_check_mode=True)

    def execute_module(self):
        state = self.params.pop('state')
        name = self.params.pop('name')
        kubeconfig = self.params.pop('kubeconfig')
        context = self.params.pop('context')
        namespace = self.params.pop('namespace', None)
        annotations = self.params.pop('annotations', None)
        labels = self.params.pop('labels', None)

        try:
            # config = self._get_client_config(kubeconfig, context)
            self._get_client_config(kubeconfig, context)
        except OpenShiftAnsibleModuleError as e:
            self.fail_json(msg='Error loading config', error=str(e))

        existing = self.helper.get_object(name, namespace)

        return_attributes = {
            'changed': False,
            'api_version': self.api_version.lower(),
            self.kind: None
        }

        if state == 'absent':
            if existing is None:
                self.exit_json(**return_attributes)
            else:
                if not self.check_mode:
                    self.helper.delete_object(name, namespace)
                return_attributes['changed'] = True
                self.exit_json(**return_attributes)
        else:
            # state == 'present'
            if existing is None:
                metadata = self.properties['metadata'](
                    name=name, annotations=annotations, labels=labels
                )

                prop_kwargs = {}
                for prop_key in list(self.properties.keys()):
                    prop_params = [
                        x for x in list(self.params.keys())
                        if x.startswith(prop_key) and self.params[x] is
                        not None
                    ]
                    if len(prop_params) > 0:
                        # print(prop_params)
                        # TODO: parse properties and set the params as appropriate
                        self.fail_json(
                            msg='Create with properties not implemented yet'
                        )

                camel_kind = string_utils.snake_case_to_camel(self.kind
                                                              ).capitalize()
                k8s_object = self.model(
                    api_version=self.api_version.lower(),
                    kind=camel_kind,
                    metadata=metadata,
                    **prop_kwargs
                )

                if not self.check_mode:
                    create_method = self.__lookup_method('create')
                    k8s_object = create_method(k8s_object)

                return_attributes[self.kind] = k8s_object.to_dict()
                return_attributes['changed'] = True
                self.exit_json(**return_attributes)
            else:
                k8s_obj = copy.deepcopy(existing)
                changed = False

                # TODO: add special casing for project, where attributes need to be updated on the namespace
                # TODO: add support for merging labels and annotations instead of overwriting
                #       will also need a way to remove particular labels with this as well
                if labels is not None and labels != existing.metadata.labels:
                    k8s_obj.metadata.labels = labels
                    changed = True

                if annotations is not None and annotations != existing.metadata.annotations:
                    k8s_obj.metadata.annotations = annotations
                    changed = True

                for prop_key in list(self.properties.keys()):
                    prop_params = [
                        x for x in list(self.params.keys())
                        if x.startswith(prop_key) and self.params[x] is
                        not None
                    ]
                    if len(prop_params) > 0:
                        # print(prop_params)
                        # TODO: compare properties and update k8s_obj as appropriate
                        self.fail_json(
                            msg='Update with properties not implemented yet'
                        )

                if changed:
                    if not self.check_mode:
                        k8s_obj.status = None
                        k8s_obj.metadata.resource_version = None
                        patch_method = self.__lookup_method('patch')
                        if self.namespaced:
                            k8s_obj = patch_method(name, namespace, k8s_obj)
                        else:
                            k8s_obj = patch_method(name, k8s_obj)
                    return_attributes[self.kind] = k8s_obj.to_dict()
                    return_attributes['changed'] = True
                else:
                    return_attributes[self.kind] = existing.to_dict()

                self.exit_json(**return_attributes)

    def __lookup_method(self, operation):
        method_name = operation
        if self.namespaced:
            method_name += '_namespaced'
        method_name += '_' + self.kind

        apis = [x for x in dir(client.apis) if VERSION_RX.search(x)]
        apis.append('OapiApi')

        for api in apis:
            api_class = getattr(client.apis, api)
            method = getattr(api_class(), method_name, None)
            if method is not None:
                break

        return method

    @classmethod
    def __properties_from_model_obj(cls, model_obj):
        model_class = type(model_obj)
        property_names = [
            x for x in dir(model_class)
            if isinstance(getattr(model_class, x), property)
        ]
        properties = {}
        for name in property_names:
            prop_kind = model_obj.swagger_types[name]
            if prop_kind == 'str':
                prop_class = str
            elif prop_kind == 'int':
                prop_class = int
            elif prop_kind.startswith('list['):
                prop_class = list
            elif prop_kind.startswith('dict('):
                prop_class = dict
            else:
                prop_class = getattr(client.models, prop_kind)

            properties[name] = prop_class
        return properties

    @staticmethod
    def __properties_from_model(model_class):
        return [
            x for x in dir(model_class)
            if isinstance(getattr(model_class, x), property)
        ]

    @staticmethod
    def _get_client_config(kubeconfig, context):
        try:
            # attempt to load the client config from file
            config.load_kube_config(config_file=kubeconfig, context=context)
        except IOError as e:
            # TODO: attempt to create client config from args
            raise OpenShiftAnsibleModuleError(
                "Cannot determine api endpoint, please specify kubeconfig",
                error=str(e)
            )
        except ConfigException as e:
            raise OpenShiftAnsibleModuleError(
                "Error generating client configuration", error=str(e)
            )
        return config

    @staticmethod
    def __get_model(api_version, kind):
        camel_kind = string_utils.snake_case_to_camel(kind).capitalize()
        model_name = api_version.capitalize() + camel_kind
        model = getattr(client.models, model_name)
        return model
