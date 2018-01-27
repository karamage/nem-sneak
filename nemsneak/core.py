# -*- coding: utf-8 -*-

import json
from contextlib import closing
from urllib import request
from codecs import getreader
from datetime import datetime, timezone
import time
import pytz


nem_epoch = datetime(2015, 3, 29, 0, 6, 25, 0, timezone.utc)
tz = pytz.timezone('Asia/Tokyo')


def dt2ts(dt):
    return int((
        tz.localize(dt).astimezone(timezone.utc) - nem_epoch
    ).total_seconds())


def ts2dt(ts):
    return pytz.utc.localize(
        datetime.fromtimestamp(ts + time.mktime(nem_epoch.timetuple()))
    ).astimezone(tz)


def get(route, param=None, base_url=None):
    base = base_url if base_url is not None else 'http://localhost:7890'
    url = base.strip('/') + '/' +\
        route.strip('/').strip('?') + (
            '?' + '&'.join((k + '=' + str(v) for k, v in param.items()))
        ) if param is not None else ''
    with closing(request.urlopen(url)) as conn:
        return json.load(getreader('utf-8')(conn))


def get_account_info(account_address, base_url=None):
    return get(
        route='account/get',
        param={'address': account_address},
        base_url=base_url
    )


def get_outgoing_tx_single(account_address, id_=None, hash_=None,
                           base_url=None):
    param = {'address': account_address}
    if id_ is not None:
        param['id'] = id_
    if hash_ is not None:
        param['hash'] = hash_
    return get(
        route='account/transfers/outgoing',
        param=param,
        base_url=base_url
    )


def get_incoming_tx_single(account_address, id_=None, hash_=None,
                           base_url=None):
    param = {'address': account_address}
    if id_ is not None:
        param['id'] = id_
    if hash_ is not None:
        param['hash'] = hash_
    return get(
        route='account/transfers/incoming',
        param=param,
        base_url=base_url
    )


def get_outgoing_tx(account_address, datetime,
                    base_url=None):
    ts = dt2ts(datetime)
    res = []
    id_ = None
    last_ts = None
    while True:
        tmp = get_outgoing_tx_single(
            account_address, id_=id_, base_url=base_url
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


def get_incoming_tx(account_address, datetime,
                    base_url=None):
    ts = dt2ts(datetime)
    res = []
    id_ = None
    last_ts = None
    while True:
        tmp = get_incoming_tx_single(
            account_address, id_=id_, base_url=base_url
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
