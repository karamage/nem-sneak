# -*- coding: utf-8 -*-


def tidy_transaction(tr, conn, sender=None):
    s_ = sender

    if tr['transaction']['type'] == 16385:
        return {
            'from_address': s_,
            'to_address': None,
            'amount': 'MosaicDefinitionCreationTransaction',
            'fee': tr['transaction']['fee'],
            'datetime': conn.ts2dt(tr['transaction']['timeStamp'])
        }
    elif tr['transaction']['type'] == 8193:
        return {
            'from_address': s_,
            'to_address': None,
            'amount': 'ProvisionNamespaceTransaction',
            'fee': tr['transaction']['fee'],
            'datetime': conn.ts2dt(tr['transaction']['timeStamp'])
        }
    elif tr['transaction']['type'] == 2049:
        return {
            'from_address': s_,
            'to_address': None,
            'amount': 'ImportanceTransferTransaction',
            'fee': tr['transaction']['fee'],
            'datetime': conn.ts2dt(tr['transaction']['timeStamp'])
        }
    elif tr['transaction']['type'] == 4097:
        return {
            'from_address': s_,
            'to_address': None,
            'amount': 'ConvertingAnAccountToMultisigAccount',
            'fee': tr['transaction']['fee'],
            'datetime': conn.ts2dt(tr['transaction']['timeStamp'])
        }
    elif tr['transaction']['type'] == 4100:
        return tidy_transaction({
            'meta': tr['meta'],
            'transaction': tr['transaction']['otherTrans']
        }, conn, sender)
    if sender is None:
        s_ = conn.pubkey2addr(tr['transaction']['signer'])
    try:
        return {
            'from_address': s_,
            'to_address': tr['transaction']['recipient'],
            'amount': tr['transaction']['amount'],
            'fee': tr['transaction']['fee'],
            'datetime': conn.ts2dt(tr['transaction']['timeStamp'])
        }
    except Exception as e:
        print(e)
        print(tr)


def pp_transaction(keys, ttr):
    return [
        '' if k not in ttr else (
            ttr[k] if k != 'datetime' else
            ttr[k].strftime('%Y-%m-%d %H:%M:%S')
        ) for k in keys
    ]
