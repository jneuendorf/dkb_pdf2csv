import argparse

from src.process import Process


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description='Process some PDF files.',
    )
    argument_parser.add_argument(
        'pdfs',
        type=str,
        nargs='+',
        help='PDF files to process',

    )
    args = argument_parser.parse_args()

    pdfs = args.pdfs
    Process().run(pdfs)
