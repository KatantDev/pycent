CENT
====

Python tools to communicate with Centrifugo v5 HTTP API. Python >= 3.9 supported.

To install run:

```bash
pip install cent
```
---
### Centrifugo compatibility

**Cent v5 and higher works only with Centrifugo v5**.

If you need to work with Centrifugo v3 then use Cent v4
If you need to work with Centrifugo v2 then use Cent v3
---
### High-level library API

First
see [available API methods in documentation](https://centrifugal.dev/docs/server/server_api#api-methods).

This library contains `CentClient` class to send messages to Centrifugo from your
python-powered backend:

```python
import asyncio
from cent import CentClient

url = "http://localhost:8000/api"
api_key = "XXX"

# Initialize client
client = CentClient(url, api_key=api_key)


async def main():
    response = await client.publish(
        "example:2",
        {"input": "Hello world!"},
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
```
---
### CentClient init arguments

Required:

* base_url - Centrifugo HTTP API endpoint address
* api_key - Centrifugo HTTP API key

Optional:

* session (`BaseSession`) - session to use

You can use `AiohttpSession` or create custom from `BaseSession` class.

Arguments for default session:

Required:

* base_url - Centrifugo HTTP API endpoint address

Optional:

* json_loads — function to load JSON from response body
* timeout - timeout for requests
