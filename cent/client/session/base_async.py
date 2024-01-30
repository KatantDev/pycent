from abc import ABC, abstractmethod
from typing import Final, TYPE_CHECKING, Callable, Any, Optional, cast

from cent.methods.base import CentMethod, CentType
from cent.client.session.base import BaseSession

if TYPE_CHECKING:
    from cent.client.async_client import AsyncClient

DEFAULT_TIMEOUT: Final[float] = 60.0
_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]


class BaseAsyncSession(BaseSession, ABC):
    """Base class for all sessions."""

    @abstractmethod
    async def close(self) -> None:
        """
        Close client session
        """

    @abstractmethod
    async def make_request(
        self,
        client: "AsyncClient",
        method: CentMethod[CentType],
        timeout: Optional[float] = None,
    ) -> CentType:
        """
        Make request to centrifuge API.

        :param client: Centrifuge client.
        :param method: Centrifuge method.
        :param timeout: Request timeout.
        """
        ...

    async def __call__(
        self,
        client: "AsyncClient",
        method: CentMethod[CentType],
        timeout: Optional[float] = None,
    ) -> CentType:
        return cast(CentType, await self.make_request(client, method, timeout))

    async def __aenter__(self) -> "BaseAsyncSession":
        return self

    async def __aexit__(self, *kwargs: Any) -> None:
        await self.close()