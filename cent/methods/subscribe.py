from typing import Optional, Any

from cent.methods.base import CentMethod
from cent.types import (
    StreamPosition,
    SubscribeResult,
    ChannelOptionsOverride,
)


class SubscribeMethod(CentMethod[SubscribeResult]):
    """Subscribe request."""

    __returning__ = SubscribeResult
    __api_method__ = "subscribe"

    user: str
    """User ID to subscribe."""
    channel: str
    """Name of channel to subscribe user to."""
    info: Optional[Any] = None
    """Attach custom data to subscription (will be used in presence and join/leave messages)."""
    b64info: Optional[str] = None
    """info in base64 for binary mode (will be decoded by Centrifugo)."""
    client: Optional[str] = None
    """Specific client ID to subscribe (user still required to be set, will ignore other user connections with different client IDs)."""
    session: Optional[str] = None
    """Specific client session to subscribe (user still required to be set)."""
    data: Optional[Any] = None
    """Custom subscription data (will be sent to client in Subscribe push)."""
    b64data: Optional[str] = None
    """Same as data but in base64 format (will be decoded by Centrifugo)."""
    recover_since: Optional[StreamPosition] = None
    """Stream position to recover from."""
    override: Optional[ChannelOptionsOverride] = None
    """Allows dynamically override some channel options defined in Centrifugo configuration (see below available fields)."""