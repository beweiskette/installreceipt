import argparse
import json
from .compare import compare, releases
from .sandbox import prepare
from .safeio import read_json, report

def main(argv=None):
    parser = argparse.ArgumentParser(description='Prepare Windows Sandbox MSI receipts and compare them locally')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare'); p.add_argument('installer'); p.add_argument('--out', required=True)
    p.add_argument('--cab', action='append', default=[], help='External CAB beside the MSI; repeat as needed')
    p.add_argument('--transform', action='append', default=[], help='MST applied in the specified order; repeat as needed')
    p = sub.add_parser('compare')
    for name in ('before', 'installed', 'removed'): p.add_argument(name)
    p.add_argument('--out', required=True)
    p = sub.add_parser('releases'); p.add_argument('a'); p.add_argument('b'); p.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'prepare':
            prepare(args.installer, args.out, cabs=args.cab, transforms=args.transform)
            print('Prepared. Open run.wsb manually on a Windows Sandbox host. The installer has not run.')
            return 0
        result = compare(*(read_json(getattr(args, n)) for n in ('before', 'installed', 'removed'))) if args.command == 'compare' else releases(read_json(args.a), read_json(args.b))
        report(result, args.out)
        print(json.dumps({'status': result.get('status', 'changed' if result.get('changed') else 'same')}))
        return int(result.get('status') == 'attention' or result.get('changed', False))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f'Cannot process receipt : {exc}. Check input format and local paths.\n')
