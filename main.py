import argparse
import datetime

from lib import update_cheaters_log


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=datetime.date.fromisoformat)
    parser.add_argument('--cheaters', type=str, default='data/cheaters.db')
    parser.add_argument('--client', type=str, default='data/client.csv')
    parser.add_argument('--server', type=str, default='data/server.csv')

    args = parser.parse_args()

    update_cheaters_log(args.date, args.cheaters, args.client, args.server)
