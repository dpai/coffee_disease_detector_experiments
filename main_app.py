import argparse
from logging import getLogger

logger = getLogger()

parser = argparse.ArgumentParser(description="Implementation of Coffee Disease Classifier")

## Data parameters
parser.add_argument("--data_path", type=str, default="/path/to/coffeedata",
                    help="path to dataset repository")

## Optimization parameters
parser.add_argument("--epochs", default=100, type=int,
                    help="number of total epochs to run")
parser.add_argument("--batch_size", default=64, type=int,
                    help="Batch size for training")

## Other parameters
parser.add_argument("--dump_path", type=str, default=".",
                    help="experiment dump path for checkpoints and log")
parser.add_argument("--seed", type=int, default=31, help="set random seed")

def main():
    global args
    args = parser.parse_args()


if __name__ == '__main__':
    main()
