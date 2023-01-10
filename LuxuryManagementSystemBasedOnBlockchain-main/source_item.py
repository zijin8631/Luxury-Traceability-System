from db import DB
from conf import db_url
import requests
import json
import time

db = DB(db_url)


def find_UTXO():
    req = requests.get(db_url+ "/block_chain/_all_docs")
    db_json = req.json()
    UTXOBlocks = []
    otherBlocks = []
    for row in db_json['rows']:
        if "UTXO" not in row['id']:
            otherBlocks.append(row)
        else:
            UTXOBlocks.append(row)
    return [UTXOBlocks,otherBlocks]

def find_belonging(item): # int input
    item_id = item
    UTXO = find_UTXO()[0]
    for row in UTXO:
        recv = db.__getitem__(row['id'])
        if recv['value'] == item_id:
            # print(recv['pub_key_hash'])
            txid = recv["_id"][4:-2]
            return [txid,recv['pub_key_hash']]
        else:
            continue
    print("Index error")

def find_txs(txid):
    previousTxid = ''
    blocks = find_UTXO()[1][:-1]  # drop the last flag
    for block in blocks:
        recv = db.__getitem__(block['id'])
        txs = recv['transactions']
        for tx in txs:
            if tx['txid'] == txid:
                previousTxid = tx['vins'][0]['txid']
                timestamp = recv['block_header']['timestamp']
                return [timestamp,tx,previousTxid]

def source_chain(item):
    txid, lastaddr = find_belonging(item)
    txPool = []
    prevTxid = txid
    while prevTxid == txid:
        timestamp, tx, prevTxid = find_txs(txid)
        tre_timeArray = time.localtime(float(timestamp))
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", tre_timeArray)
        addr = tx['vouts'][0]['pub_key_hash']
        txPool.append([timestr,addr])
        if prevTxid == '':
            break
        txid = prevTxid
    return txPool










