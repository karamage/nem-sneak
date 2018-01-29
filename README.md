# nem-sneak

## nem-docker setup

```
git clone https://github.com/rb2nem/nem-docker.git
cd nem-docker
docker build -t nem-nis .
cp custom-configs/supervisord.conf.sample custom-configs/supervisord.conf
vim custom-configs/supervisord.conf
----以下のように編集-----
...
[program:nis]
user=nem
autostart=true
directory=/package/nis
...
-------------------------------

docker run --rm -d -p 7890:7890 -v "nem_data:/home/nem/nem" -v "$PWD/custom-configs/supervisord.conf:/etc/supervisord.conf" --name nem nem-nis
```

## installation

```
pip install git+https://github.com/ozcn/nem-sneak.git
```

or

```
git clone https://github.com/ozcn/nem-sneak.git
cd nem-sneak
pip install .
```

## nem-sneak basic usage

```python
import nemsneak
import pytz
from datetime import datetime

conn = nemsneak.Connection(pytz.timezone('Asia/Tokyo'), 'http://your_nis_address:7890')
conn.get('/status') # access /status route of NIS API
conn.get('/account/get', {'address': 'NC4C6PSUW5CLTDT5SXAGJDQJGZNESKFK5MCN77OG'}) # access /account/get route with address=NC4C6PSUW5CLTDT5SXAGJDQJGZNESKFK5MCN77OG get parameter
conn.get_account_info('NC4C6PSUW5CLTDT5SXAGJDQJGZNESKFK5MCN77OG') # get current status of 'NC4C6PSUW5CLTDT5SXAGJDQJGZNESKFK5MCN77OG'
conn.get_all_tx('NC4C6PSUW5CLTDT5SXAGJDQJGZNESKFK5MCN77OG', datetime(2018, 1, 26, 0, 2, 13)) # get all transaction of 'NC4C6PSUW5CLTDT5SXAGJDQJGZNESKFK5MCN77OG' from 2018/01/26 00:02:13

g = nemsneak.Gazer('NC4C6PSUW5CLTDT5SXAGJDQJGZNESKFK5MCN77OG', conn, lambda addr, tx: print((addr, tx))) # create a transaction monitor instance which prints new transactions of 'NC4C6PSUW5CLTDT5SXAGJDQJGZNESKFK5MCN77OG'.
g.start() # start the monitor thread
```
