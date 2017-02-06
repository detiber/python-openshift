import re

import string_utils

from kubernetes import config
from kubernetes.client.rest import ApiException
from openshift import client

#: Regex for finding versions
VERSION_RX = re.compile("V\d((alpha|beta)\d)?")


class KubernetesObjectHelper(object):
    def __init__(self, api_version, kind):
        self.api_version = api_version
        self.kind = kind
        self.model = self.__get_model(api_version, kind)

        # TODO: handle config better than just using default kubeconfig
        config.load_kube_config()

    def get_object(self, name, namespace=None):
        k8s_obj = None
        try:
            if namespace is None:
                get_method = self.__lookup_method('read', False)
                k8s_obj = get_method(name)
            else:
                get_method = self.__lookup_method('read', True)
                k8s_obj = get_method(name, namespace)
        except ApiException as e:
            if e.status != 404:
                raise
        return k8s_obj

    def delete_object(self, name, namespace=None):
        # TODO: add a parameter for waiting until the object has been deleted
        # TODO: deleting a namespace requires a body
        k8s_obj = None
        try:
            if namespace is None:
                get_method = self.__lookup_method('delete', False)
                k8s_obj = get_method(name)
            else:
                get_method = self.__lookup_method('delete', True)
                k8s_obj = get_method(name, namespace)
        except ApiException as e:
            if e.status != 404:
                raise

    def __lookup_method(self, operation, namespaced):
        # TODO: raise error if method not found
        method_name = operation
        if namespaced:
            method_name += '_namespaced'
        method_name += '_' + self.kind

        apis = [x for x in dir(client.apis) if VERSION_RX.search(x)]
        apis.append('OapiApi')

        method = None

        for api in apis:
            api_class = getattr(client.apis, api)
            method = getattr(api_class(), method_name, None)
            if method is not None:
                break

        return method

    @staticmethod
    def __get_model(api_version, kind):
        camel_kind = string_utils.snake_case_to_camel(kind).capitalize()
        model_name = api_version.capitalize() + camel_kind
        model = getattr(client.models, model_name)
        return model
