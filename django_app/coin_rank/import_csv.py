import sqlite3 as lite
import csv
import os
from zero0 import read_csv

con = lite.connect('db.sqlite3')
cur = con.cursor()
# cur.execute('SELECT SQLITE_VERSION()')
# data = cur.fetchone()
# print("SQLite version: %s" % data)
csv_file_loc = "csv/0x.csv"
all_the_records,top_timestamp_token_holder_dict = read_csv(csv_file_loc)

for timestamp in all_the_records:
    transactions = all_the_records[timestamp]
    # print(timestamp)
    #timestamp
    timestamp_sql = "INSERT INTO polls_timestamp (daily_timestamp) SELECT (?) WHERE NOT EXISTS(SELECT 1 FROM polls_timestamp WHERE daily_timestamp = (?))"
    cur.execute(timestamp_sql,(timestamp,timestamp))
    cur.execute("SELECT id from polls_timestamp WHERE daily_timestamp = (?)",(timestamp,))
    daily_timestamp_id = cur.fetchone()[0]

    for transaction in transactions:
        #from account
        gussed_name = "empty"
        from_account_sql = "INSERT INTO polls_account (gussed_name,account_address) SELECT (?),(?) WHERE NOT EXISTS(SELECT 1 FROM polls_account WHERE account_address = (?))"
        cur.execute(from_account_sql,(gussed_name,transaction.from_account,transaction.from_account))
        cur.execute("SELECT id from polls_account WHERE account_address = (?)",(transaction.from_account,))
        from_account_address_id = cur.fetchone()[0]

        #to account
        cur.execute(from_account_sql,(gussed_name,transaction.to_account,transaction.to_account))
        to_account_address_id = cur.lastrowid
        cur.execute("SELECT id from polls_account WHERE account_address = (?)",(transaction.to_account,))
        to_account_address_id = cur.fetchone()[0]

        # print("from_account_address_id:{}".format(from_account_address_id))
        # print("to_account_address_id:{}".format(to_account_address_id))

        #transaction_obj
        transaction_sql = "INSERT INTO polls_tokentransaction (tx_hash,quantity,from_account_id,to_account_id,token_name_id,timestamp_id) SELECT (?),(?),(?),(?),(?),(?) WHERE NOT EXISTS(SELECT 1 FROM polls_tokentransaction WHERE tx_hash = (?))"
        cur.execute(transaction_sql,(transaction.tx_hash,transaction.quantity,from_account_address_id,to_account_address_id,37,daily_timestamp_id,transaction.tx_hash))

    con.commit()
    print("daily_timestamp_id:{}".format(daily_timestamp_id))

cur.close()
con.close()
