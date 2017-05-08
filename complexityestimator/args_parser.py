from argparse import ArgumentParser


parser = ArgumentParser(
        description='complexity estimator')

parser.add_argument(
    'main',
    help='main function to test')

parser.add_argument(
    '-i', '--initialize',
    help='file name with initialized structures')

parser.add_argument(
    '-c', '--clean',
    help='file name free resources')

parser.add_argument(
    '-t', '--timeout',
    type=int,
    default=30,
    help='max time')