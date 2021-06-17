import argparse
import datetime

from lib import update_cheaters_log


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=datetime.date.fromisoformat)
    parser.add_argument('--cheaters', type=str, default='data/cheaters.db')

    args = parser.parse_args()

    update_cheaters_log(args.date, args.cheaters)
