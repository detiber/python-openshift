import pytest


@pytest.mark.ansible(host_pattern='localhost', connection='local')
def test_namespace_delete_noop(ansible_module):
    contacted = ansible_module.k8s_namespace(
        name='test',
        state='absent',
        api_version='v1'
    )

    for host, result in contacted.items():
        assert 'failed' not in result, result['msg']
        assert 'changed' in result
        assert result['changed'] is False
