# -*- coding: utf-8 -*-

import json
from contextlib import closing
from urllib import request
from codecs import getreader
from datetime import datetime, timezone
import time
import pytz


nem_epoch = datetime(2015, 3, 29, 0, 6, 25, 0, timezone.utc)


class Connection(object):
    """Connection to NIS

    :param tz: your timezone (default: ``timezone.utc``)
    :param base_url: base url for the NIS \
    (default: ``'http://localhost:7890'``)
    """
    def __init__(self, tz=None, base_url=None):
        super(Connection, self).__init__()
        self.tz = tz if tz is not None else timezone.utc
        self.base_url = base_url if base_url is not None else \
            'http://localhost:7890'

    def dt2ts(self, dt):
        """convert datetime to NEM timeStamp

        :param dt: datetime
        """
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            return int((
                self.tz.localize(dt).astimezone(timezone.utc) - nem_epoch
            ).total_seconds())
        else:
            return int((
                dt.astimezone(timezone.utc) - nem_epoch
            ).total_seconds())

    def ts2dt(self, ts):
        """convert NEM timeStamp to tz aware datetime

        :param ts: NEM timeStamp
        """
        return pytz.utc.localize(
            datetime.fromtimestamp(ts + time.mktime(nem_epoch.timetuple()))
        ).astimezone(self.tz)

    def num2nem(self, num):
        return num / 1000000

    def pubkey2addr(self, pubkey):
        return self.get(
            '/account/get/from-public-key',
            {'publicKey': pubkey}
        )['account']['address']

    def get(self, route, param=None):
        """get request

        :param route: API route
        :param param: get parameters (dict)
        """
        url = self.base_url.strip('/') + '/' +\
            route.strip('/').strip('?') + ((
                '?' + '&'.join((k + '=' + str(v) for k, v in param.items()))
            ) if param is not None else '')
        with closing(request.urlopen(url)) as conn:
            return json.load(getreader('utf-8')(conn))

    def get_account_info(self, account_address):
        """get account info from /account/get route

        :param account_address: the address of the account
        """
        return self.get(
            route='account/get',
            param={'address': account_address}
        )

    def get_tx_single(self, type_, account_address, id_=None, hash_=None):
        """get maximum of 25 transaction data.

        :param type_: transaction type. one of 'all', 'incoming', 'outgoing'
        :param account_address: the address of the account
        :param id_: The transaction id up to which transactions are returned.
        :param hash_: The 256 bit sha3 hash of the transaction up to which \
            transactions are returned.
        """
        param = {'address': account_address}
        if id_ is not None:
            param['id'] = id_
        if hash_ is not None:
            param['hash'] = hash_
        return self.get(
            route='account/transfers/' + type_,
            param=param
        )

    def get_outgoing_tx_single(self, account_address, id_=None, hash_=None):
        """get maximum of 25 outgoing transaction data.

        :param account_address: the address of the account
        :param id_: The transaction id up to which transactions are returned.
        :param hash_: The 256 bit sha3 hash of the transaction up to which \
            transactions are returned.
        """
        return self.get_tx_single('outgoing', account_address, id_, hash_)

    def get_incoming_tx_single(self, account_address, id_=None, hash_=None):
        """get maximum of 25 incoming transaction data.

        :param account_address: the address of the account
        :param id_: The transaction id up to which transactions are returned.
        :param hash_: The 256 bit sha3 hash of the transaction up to which \
            transactions are returned.
        """
        return self.get_tx_single('incoming', account_address, id_, hash_)

    def get_all_tx_single(self, account_address, id_=None, hash_=None):
        """get maximum of 25 transaction data.

        :param account_address: the address of the account
        :param id_: The transaction id up to which transactions are returned.
        :param hash_: The 256 bit sha3 hash of the transaction up to which \
            transactions are returned.
        """
        return self.get_tx_single('all', account_address, id_, hash_)

    def get_tx_loop(self, type_, account_address, dt_from):
        """get the transaction data after ``dt_from``

        :param type_: transaction type. one of 'all', 'incoming', 'outgoing'
        :param account_address: the address of the account
        :param dt_from: native datetime
        """
        ts = self.dt2ts(dt_from)
        res = []
        id_ = None
        last_ts = None
        while True:
            tmp = self.get_tx_single(
                type_, account_address, id_=id_
            )
            if len(tmp['data']) == 0:
                break
            for d in tmp['data']:
                _t = d['transaction']['timeStamp']
                if _t >= ts:
                    res.append(d)
                if last_ts is None or last_ts > _t:
                    last_ts = _t
                    id_ = d['meta']['id']
            if last_ts < ts:
                break
            else:
                time.sleep(0.1)
        return res

    def get_outgoing_tx(self, account_address, dt_from):
        """get the outgoing transaction data after ``dt_from``

        :param account_address: the address of the account
        :param dt_from: native datetime
        """
        return self.get_tx_loop('outgoing', account_address, dt_from)

    def get_incoming_tx(self, account_address, dt_from):
        """get the incoming transaction data after ``dt_from``

        :param account_address: the address of the account
        :param dt_from: native datetime
        """
        return self.get_tx_loop('incoming', account_address, dt_from)

    def get_all_tx(self, account_address, dt_from):
        """get the transaction data after ``dt_from``

        :param account_address: the address of the account
        :param dt_from: native datetime
        """
        return self.get_tx_loop('all', account_address, dt_from)
