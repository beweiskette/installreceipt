import json
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest
from installreceipt.compare import compare, releases
from installreceipt.sandbox import prepare

def snap(**items):
    return {'schema': 1, 'complete': True, 'items': items}

def test_install_changes_and_uninstall_residue():
    before = snap(path='a' * 64)
    installed = snap(path='b' * 64, service='c' * 64)
    removed = snap(path='a' * 64, service='c' * 64)
    result = compare(before, installed, removed)
    assert result['installation']['added'] == ['service']
    assert result['installation']['changed'] == ['path']
    assert result['uninstall_residue']['added'] == ['service']
    assert result['status'] == 'attention'
    assert releases(result, compare(before, installed, before))['changed']

def test_incomplete_and_plain_values_refused():
    with pytest.raises(ValueError):
        compare({'schema': 1, 'complete': False, 'items': {}}, snap(), snap())
    with pytest.raises(ValueError):
        compare(snap(secret='PLAINTEXT'), snap(), snap())

def test_sandbox_is_explicit_and_restricted(tmp_path):
    msi = tmp_path / 'demo & test.msi'
    msi.write_bytes(b'SYNTHETIC_NOT_A_REAL_INSTALLER')
    out = tmp_path / 'package'
    prepare(msi, out)
    root = ET.parse(out / 'run.wsb').getroot()
    assert root.findtext('Networking') == 'Disable'
    assert root.findtext('ClipboardRedirection') == 'Disable'
    maps = root.findall('MappedFolders/MappedFolder')
    assert [x.findtext('ReadOnly') for x in maps] == ['true', 'false']
    assert Path(maps[1].findtext('HostFolder')) == out / 'output'
    assert (out / 'input' / 'installer.msi').read_bytes() == msi.read_bytes()
    with pytest.raises(ValueError):
        prepare(msi, out)
