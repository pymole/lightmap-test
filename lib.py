import sqlite3
from sqlite3 import Connection
from typing import Iterable
import datetime

import pandas as pd
from pandas import DataFrame


def load_client(date: datetime.date, client_path: str) -> DataFrame:
    client = pd.read_csv(client_path)
    client.rename(columns={'description': 'json_client'}, inplace=True)
    client['timestamp'] = pd.to_datetime(client['timestamp'], unit='s')
    client = client[client['timestamp'].dt.date == date]
    client.drop(columns=['timestamp'], inplace=True)
    return client


def load_server(date: datetime.date, server_path: str) -> DataFrame:
    server = pd.read_csv(server_path)
    server.rename(columns={'description': 'json_server'}, inplace=True)
    server['timestamp'] = pd.to_datetime(server['timestamp'], unit='s')
    server = server[server['timestamp'].dt.date == date]

    return server


def get_log(date: datetime.date, client_path: str, server_path: str) -> DataFrame:
    client = load_client(date, client_path)
    server = load_server(date, server_path)
    log = pd.merge(client, server, on='error_id')

    return log


def load_cheaters(conn: Connection, player_ids: Iterable[int]) -> DataFrame:
    return pd.read_sql_query(
        f"SELECT * from cheaters where player_id in ({', '.join(str(player_id) for player_id in player_ids)})",
        conn,
        parse_dates=['ban_time']
    )


def get_cheaters_from_log(date: datetime.date, client_path: str, server_path: str,
                          cheaters_conn: Connection) -> DataFrame:
    log = get_log(date, client_path, server_path)
    cheaters = load_cheaters(cheaters_conn, set(log.player_id))
    log_cheaters = pd.merge(log, cheaters, on='player_id')
    log_cheaters = log_cheaters[log_cheaters['ban_time'].dt.date < log_cheaters['timestamp'].dt.date]
    log_cheaters.drop(columns=['ban_time'], inplace=True)

    return log_cheaters


def update_cheaters_log(date: datetime.date, cheaters_path: str, client_path: str, server_path: str):
    cheaters_conn = sqlite3.connect(cheaters_path)

    log_cheaters = get_cheaters_from_log(date, client_path, server_path, cheaters_conn)
    log_cheaters['timestamp'] = log_cheaters['timestamp'].values.astype(int) / 10**9
    log_cheaters.to_sql('log', con=cheaters_conn, if_exists='append', index=False)

    cheaters_conn.close()
