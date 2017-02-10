import pytest
import yaml

pytestmark = pytest.mark.ansible


# TODO: ensure created namespaces are cleaned up
# TODO: ensure created namespaces are cleaned up
# TODO: use auto-generated names
@pytest.mark.ansible(host_pattern='localhost', connection='local')
def test_project_delete_noop(ansible_module):
    contacted = ansible_module.openshift_v1_project(
        name='test_delete_noop', state='absent'
    )

    for host in contacted.keys():
        result = contacted[host]
        print(yaml.dump(result))
        assert 'failed' not in result.keys()
        assert 'changed' in result.keys()
        assert result['changed'] is False


@pytest.mark.ansible(host_pattern='localhost', connection='local')
def test_project_lifecycle(ansible_module):
    contacted = ansible_module.openshift_v1_project(
        name='test-project-lifecycle', state='present'
    )

    for host in contacted.keys():
        result = contacted[host]
        print(yaml.dump(result))
        assert 'failed' not in result.keys()
        assert 'changed' in result.keys()
        assert result['changed'] is True

    contacted = ansible_module.openshift_v1_project(
        name='test-project-lifecycle', state='present'
    )

    for host in contacted.keys():
        result = contacted[host]
        print(yaml.dump(result))
        assert 'failed' not in result.keys()
        assert 'changed' in result.keys()
        assert result['changed'] is False

    contacted = ansible_module.openshift_v1_project(
        name='test-project-lifecycle', state='absent'
    )

    for host in contacted.keys():
        result = contacted[host]
        print(yaml.dump(result))
        assert 'failed' not in result.keys()
        assert 'changed' in result.keys()
        assert result['changed'] is True
