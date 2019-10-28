import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_files(host):
    files = [
        "/etc/trickster",
        "/etc/systemd/system/trickster.service",
        "/usr/local/bin/trickster"
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_user(host):
    assert host.group("trickster").exists
    assert "trickster" in host.user("trickster").groups
    assert host.user("trickster").shell == "/usr/sbin/nologin"
    assert host.user("trickster").home == "/"


def test_service(host):
    s = host.service("trickster")
#    assert s.is_enabled
    assert s.is_running


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:8082"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
