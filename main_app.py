import argparse
from logging import getLogger

logger = getLogger()

parser = argparse.ArgumentParser(description="Implementation of Coffee Disease Classifier")

## Data parameters
parser.add_argument("--data_path", type=str, default="/path/to/coffeedata",
                    help="path to dataset repository")
build_or_load_group = parser.add_mutually_exclusive_group(required=True)
build_or_load_group.add_argument("--build_data", type=str,
                                 help="Build data per specification mentioned by string")
build_or_load_group.add_argument("--load_data", type=str,
                                 help="Load Train/Val/Test split from CSV")

## Optimization parameters
parser.add_argument("--epochs", default=100, type=int,
                    help="number of total epochs to run")
parser.add_argument("--batch_size", default=64, type=int,
                    help="Batch size for training")

## Other parameters
parser.add_argument("--dump_path", type=str, default=".",
                    help="experiment dump path for checkpoints and log")
parser.add_argument("--seed", type=int, default=31, help="set random seed")

def printArguments(args):
    print(args.data_path)
    print(args.build_data)
    print(args.load_data)
    print(args.epochs)
    print(args.batch_size)

def main():
    global args
    args = parser.parse_args()
    printArguments(args)


if __name__ == '__main__':
    main()
