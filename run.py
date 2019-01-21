import argparse
import sys

from dataset import DataSet
from algorithm import mine_rules


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file', '-f',
        dest='file_path',
        type=str,
        help='Path to data file',
        required=True,
    )
    parser.add_argument(
        '--minsupp', '-s',
        dest='min_supp',
        type=float,
        help='Minimal support',
        required=True,
    )
    parser.add_argument(
        '--minconf', '-c',
        dest='min_conf',
        type=float,
        help='Minimal confidence',
        required=True,
    )
    parser.add_argument(
        '--mincorr', '-d',
        dest='min_corr',
        type=float,
        default=0.5,
        help='Minimal correlation coefficient',
        required=False,
    )
    parser.add_argument(
        '--length', '-l',
        dest='max_len',
        type=int,
        default=None,
        help='Minimal correlation coefficient',
        required=False,
    )
    parser.add_argument(
        '--verbose', '-v',
        dest='verbose',
        action='store_true',
        help='Print to output some info during algorithm work'
    )
    return parser


if __name__ == '__main__':
    parser = get_argparser()
    args = parser.parse_args()

    ds = DataSet.from_csv(args.file_path)
    rules = mine_rules(
        dataset=ds,
        min_support=args.min_supp,
        min_confidence=args.min_conf,
        min_corr=args.min_corr,
        max_len=args.max_len,
        verbose=args.verbose,
    )

    for rule in rules:
        print(rule)
