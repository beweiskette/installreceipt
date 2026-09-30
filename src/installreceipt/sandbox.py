import shutil
import xml.etree.ElementTree as ET
from importlib.resources import files
from .safeio import local_path

def prepare(installer, directory):
    installer = local_path(installer)
    if installer.suffix.lower() != '.msi' or not installer.is_file():
        raise ValueError('A local MSI file is required')
    out = local_path(directory, exists=False)
    if out.exists():
        raise ValueError('Output directory must be new')
    inputs, outputs = out / 'input', out / 'output'
    inputs.mkdir(parents=True)
    outputs.mkdir()
    shutil.copyfile(installer, inputs / 'installer.msi')
    for name in ('collect.ps1', 'run.ps1'):
        (inputs / name).write_text(files('installreceipt').joinpath('scripts', name).read_text(encoding='utf-8'), encoding='utf-8-sig')
    root = ET.Element('Configuration')
    for key in ('Networking', 'ClipboardRedirection', 'PrinterRedirection', 'AudioInput', 'VideoInput', 'vGPU'):
        ET.SubElement(root, key).text = 'Disable'
    ET.SubElement(root, 'MemoryInMB').text = '2048'
    mappings = ET.SubElement(root, 'MappedFolders')
    for host, guest, readonly in [(inputs, r'C:\ReceiptInput', 'true'), (outputs, r'C:\ReceiptOutput', 'false')]:
        mapping = ET.SubElement(mappings, 'MappedFolder')
        ET.SubElement(mapping, 'HostFolder').text = str(host)
        ET.SubElement(mapping, 'SandboxFolder').text = guest
        ET.SubElement(mapping, 'ReadOnly').text = readonly
    logon = ET.SubElement(root, 'LogonCommand')
    ET.SubElement(logon, 'Command').text = r'powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\ReceiptInput\run.ps1'
    ET.indent(root)
    ET.ElementTree(root).write(out / 'run.wsb', encoding='utf-8', xml_declaration=True)
    return out
