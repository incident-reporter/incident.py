
# Incident.py

Incident.py is a python library for creating incidents in discord.

## Installing

Incident.py is currently *not* on PyPi, but you can use the commad below to install it with pip.

```sh
pip install git+https://git@github.com/incident-reporter/incident.py.git
```

If you need a specific version, use `@`

```sh
pip install git+https://git@github.com/incident-reporter/incident.py.git@v0.1.0
```


## Creating incidents

For creating an Incident you need to choose a http library.

### [httpx](https://github.com/encode/httpx)

Async and sync.

```python
import incident
from incident.httpx import HttpxIncident

inc = HttpxIncident('webhook')
inc.update(incident.STATE_OUTAGE, 'Something went wrong', submit=False)
inc.update(incident.STATE_RESOLVED, 'Something went right')
```

```python
import asyncio
import incident
from incident.httpx import HttpxAsyncIncident


async def main():
    inc = HttpxAsyncIncident('webhook')
    inc.update(incident.STATE_OUTAGE, 'Something went wrong', submit=False)
    await inc.update(incident.STATE_RESOLVED, 'Something went right')


asyncio.run(main())
```

### [aiohttp](https://github.com/aio-libs/aiohttp)

```python
import asyncio
import incident
from incident.aiohttp import AiohttpIncident


async def main():
    inc = AiohttpIncident('webhook')
    inc.update(incident.STATE_OUTAGE, 'Something went wrong', submit=False)
    await inc.update(incident.STATE_RESOLVED, 'Something went right')


asyncio.run(main())
```

### [requests](https://github.com/psf/requests)


```python
import incident
from incident.requests import RequestsIncident

inc = RequestsIncident('webhook')
inc.update(incident.STATE_OUTAGE, 'Something went wrong', submit=False)
inc.update(incident.STATE_RESOLVED, 'Something went right')
```