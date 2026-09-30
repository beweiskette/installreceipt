import re

def validate(value):
    if not isinstance(value, dict) or value.get('schema') != 1 or value.get('complete') is not True:
        raise ValueError('Incomplete or unsupported snapshot')
    items = value.get('items')
    if not isinstance(items, dict) or any(not isinstance(k, str) or not isinstance(v, str) or not re.fullmatch('[0-9a-f]{64}', v) for k, v in items.items()):
        raise ValueError('Snapshot values must be SHA-256 hashes')
    return items

def delta(a, b):
    return {'added': sorted(b.keys() - a.keys()), 'removed': sorted(a.keys() - b.keys()),
            'changed': sorted(k for k in a.keys() & b.keys() if a[k] != b[k])}

def compare(before, installed, removed):
    a, b, c = (validate(s) for s in (before, installed, removed))
    residue = delta(a, c)
    return {'schema': 1, 'kind': 'installation-receipt',
            'status': 'attention' if any(residue.values()) else 'pass',
            'installation': delta(a, b), 'uninstall_residue': residue,
            'installed_fingerprints': b,
            'scope': 'Selected registry trees, services and machine/user PATH. Files and all other system state are outside this version.'}

def releases(a, b):
    for receipt in (a, b):
        if receipt.get('schema') != 1 or receipt.get('kind') != 'installation-receipt':
            raise ValueError('Two installation receipts are required')
        validate({'schema': 1, 'complete': True, 'items': receipt.get('installed_fingerprints')})
    differences = delta(a['installed_fingerprints'], b['installed_fingerprints'])
    # Include changed residue findings even when installed state is identical.
    return {'schema': 1, 'kind': 'release-comparison',
            'changed': bool(any(differences.values()) or a['uninstall_residue'] != b['uninstall_residue']),
            'installed_difference': differences, 'residue_a': a['uninstall_residue'], 'residue_b': b['uninstall_residue']}
