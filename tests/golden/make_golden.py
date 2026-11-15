"""Write tests/golden/expected/ from the current code (see tests/golden/README.md).

Run on the reference machine, and only after a change that is meant to move numbers (marked ▲ in the
changelog). ``--table`` rewrites the named tables alone, so the rest keep the values they were pinned with.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tests.golden.outputs import TABLES, write_expected  # noqa: E402

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--family', choices=['continuous'],
                        help='rewrite the continuous-response values instead')
    parser.add_argument('--table', nargs='+', choices=TABLES, metavar='TABLE',
                        help=f'rewrite only these 2-AFC tables, one or more of: {", ".join(TABLES)}')
    args = parser.parse_args()
    if args.family and args.table:
        parser.error('--table names 2-AFC tables; it cannot be combined with --family')
    if args.family == 'continuous':
        from tests.golden.continuous.outputs import write_expected as write_continuous  # noqa: E402
        write_continuous()
    else:
        write_expected(args.table)
