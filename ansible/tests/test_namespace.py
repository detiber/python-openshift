import pytest
import yaml

pytestmark = pytest.mark.ansible


# TODO: ensure created namespaces are cleaned up
# TODO: use auto-generated names
@pytest.mark.ansible(host_pattern='localhost', connection='local')
def test_namespace_delete_noop(ansible_module):
    contacted = ansible_module.k8s_v1_namespace(
        name='test_delete_noop', state='absent'
    )

    for host in contacted.keys():
        result = contacted[host]
        print(yaml.dump(result))
        assert 'failed' not in result.keys()
        assert 'changed' in result.keys()
        assert result['changed'] is False


@pytest.mark.skip()
@pytest.mark.ansible(host_pattern='localhost', connection='local')
def test_namespace_lifecycle(ansible_module):
    contacted = ansible_module.k8s_v1_namespace(
        name='test-namespace-lifecycle', state='present'
    )

    for host in contacted.keys():
        result = contacted[host]
        print(yaml.dump(result))
        assert 'failed' not in result.keys()
        assert 'changed' in result.keys()
        assert result['changed'] is True

    contacted = ansible_module.k8s_v1_namespace(
        name='test-namespace-create', state='present'
    )

    for host in contacted.keys():
        result = contacted[host]
        print(yaml.dump(result))
        assert 'failed' not in result.keys()
        assert 'changed' in result.keys()
        assert result['changed'] is False

    contacted = ansible_module.k8s_v1_namespace(
        name='test-namespace-create', state='absent'
    )

    for host in contacted.keys():
        result = contacted[host]
        print(yaml.dump(result))
        assert 'failed' not in result.keys()
        assert 'changed' in result.keys()
        assert result['changed'] is True
