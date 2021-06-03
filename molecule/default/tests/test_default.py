
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
import pytest
import os
import testinfra.utils.ansible_runner

import pprint
pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def base_directory():
    cwd = os.getcwd()

    if('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(
            os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


@pytest.fixture()
def get_vars(host):
    """

    """
    base_dir, molecule_dir = base_directory()

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(
        base_dir)
    file_vars = "file={}/vars/main.yml name=role_vars".format(base_dir)
    file_molecule = "file={}/group_vars/all/vars.yml name=test_vars".format(
        molecule_dir)

    defaults_vars = host.ansible("include_vars", file_defaults).get(
        "ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get(
        "ansible_facts").get("role_vars")
    molecule_vars = host.ansible("include_vars", file_molecule).get(
        "ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def test_files(host, get_vars):
    config_file = get_vars.get("trickster_service_config").get("config_file")
    version = get_vars.get("trickster_version")

    files = []
    files.append(config_file)
    files.append("/usr/local/bin/trickster_{0}".format(version))
    files.append("/lib/systemd/system/trickster.service")

    for file in files:
        f = host.file(file)
        assert f.is_file


def test_user(host):
    assert host.group("trickster").exists
    assert "trickster" in host.user("trickster").groups
    assert host.user("trickster").shell == "/usr/sbin/nologin"
    assert host.user("trickster").home == "/nonexistent"


def test_service(host):
    s = host.service("trickster")
    assert s.is_enabled
    assert s.is_running


@pytest.mark.parametrize("ports", [
    '127.0.0.1:8480',
    '127.0.0.1:8481',
    '127.0.0.1:8484',
])
def test_open_port(host, ports):

    for i in host.socket.get_listening_sockets():
        print(i)

    service = host.socket("tcp://{}".format(ports))
    assert service.is_listening
