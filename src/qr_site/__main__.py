from pathlib import Path
from argparse import ArgumentParser
from .main import main

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('config_file', type=Path)
    parser.add_argument('-l', '--listen', type=str)
    args = parser.parse_args()
    if args.listen:
        host, port = args.listen.split(':')
        main(args.config_file, host, port)
    else:
        main(args.config_file)