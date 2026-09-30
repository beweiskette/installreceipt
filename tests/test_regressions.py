import json
import xml.etree.ElementTree as ET
from pathlib import Path
import pytest
from installreceipt.cli import main
from installreceipt.sandbox import prepare

@pytest.mark.parametrize('command,value', [('releases',[]),('releases',None),('releases',{'schema':1,'kind':'installation-receipt','installed_fingerprints':{},'uninstall_residue':'bad'}),('compare',[])])
def test_malformed_inputs_exit_two_with_reason(tmp_path,capsys,command,value):
    f=tmp_path/'bad.json'; f.write_text(json.dumps(value))
    with pytest.raises(SystemExit) as error:
        main([command]+[str(f)]*(3 if command=='compare' else 2)+['--out',str(tmp_path/'out')])
    assert error.value.code == 2
    text=capsys.readouterr().err
    assert 'required' in text or 'snapshot' in text.lower() or 'residue' in text.lower()
    assert 'Traceback' not in text

def test_xml_escapes_actual_host_mapping(tmp_path):
    msi=tmp_path/'demo.msi'; msi.write_bytes(b'synthetic')
    out=tmp_path/'package & receipt'
    prepare(msi,out)
    raw=(out/'run.wsb').read_text()
    assert 'package &amp; receipt' in raw
    root=ET.fromstring(raw)
    assert Path(root.findtext('MappedFolders/MappedFolder/HostFolder')) == out/'input'

def test_external_cab_and_transform_are_packaged(tmp_path):
    msi=tmp_path/'demo.msi'; msi.write_bytes(b'synthetic')
    cab=tmp_path/'data.cab'; cab.write_bytes(b'cab')
    mst=tmp_path/'custom.mst'; mst.write_bytes(b'mst')
    out=tmp_path/'package'
    prepare(msi,out,cabs=[cab],transforms=[mst])
    assert (out/'input/data.cab').read_bytes()==b'cab'
    assert (out/'input/custom.mst').read_bytes()==b'mst'
    assert json.loads((out/'input/install-options.json').read_text())['transforms']==['custom.mst']
    assert 'TRANSFORMS=' in (out/'input/run.ps1').read_text(encoding='utf-8-sig')
