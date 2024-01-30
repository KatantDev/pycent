import asyncio
from typing import Optional, TYPE_CHECKING, cast, Any

from aiohttp import ClientSession
from aiohttp.hdrs import USER_AGENT, CONTENT_TYPE
from aiohttp.http import SERVER_SOFTWARE

from cent.__meta__ import __version__
from cent.client.session.base_async import BaseAsyncSession
from cent.methods.base import CentMethod, CentType

if TYPE_CHECKING:
    from cent.client.async_client import AsyncClient


class AiohttpSession(BaseAsyncSession):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._session: Optional[ClientSession] = None

    async def _create_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                headers={
                    USER_AGENT: f"{SERVER_SOFTWARE} pycent/{__version__}",
                    CONTENT_TYPE: "application/json",
                    "X-Centrifugo-Error-Mode": "transport",
                },
            )

        return self._session

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

            # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
            await asyncio.sleep(0)

    async def make_request(
        self,
        client: "AsyncClient",
        method: CentMethod[CentType],
        timeout: Optional[float] = None,
    ) -> CentType:
        session = await self._create_session()
        session.headers["X-API-Key"] = client.api_key
        json_data = method.model_dump(exclude_none=True)

        url = f"{self._base_url}/{method.__api_method__}"

        async with session.post(
            url=url,
            json=json_data,
            timeout=timeout or self._timeout,
        ) as resp:
            raw_result = await resp.text()
        response = self.check_response(
            client=client,
            method=method,
            status_code=resp.status,
            content=raw_result,
        )
        return cast(CentType, response.result)

    def __del__(self) -> None:
        if self._session and not self._session.closed:
            if self._session.connector is not None and self._session.connector_owner:
                self._session.connector.close()
            self._session._connector = None