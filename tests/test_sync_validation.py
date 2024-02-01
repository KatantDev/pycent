from base64 import b64encode
from cent import Client
from cent.types import StreamPosition, Disconnect


def test_publish(sync_client: Client) -> None:
    sync_client.publish(
        "personal:1",
        {"data": "data"},
        skip_history=False,
        tags={"tag": "tag"},
        b64data=b64encode(b"data").decode(),
        idempotency_key="idempotency_key",
    )


def test_broadcast(sync_client: Client) -> None:
    sync_client.broadcast(
        ["personal:1", "personal:2"],
        {"data": "data"},
        skip_history=False,
        tags={"tag": "tag"},
        b64data=b64encode(b"data").decode(),
        idempotency_key="idempotency_key",
    )


def test_subscribe(sync_client: Client) -> None:
    sync_client.subscribe(
        "user",
        "personal:1",
        info={"info": "info"},
        b64info=b64encode(b"info").decode(),
        client="client",
        session="session",
        data={"data": "data"},
        recover_since=StreamPosition(
            offset=1,
            epoch="1",
        ),
    )


def test_unsubscribe(sync_client: Client) -> None:
    sync_client.unsubscribe(
        user="user",
        channel="personal:1",
        session="session",
        client="client",
    )


def test_presence(sync_client: Client) -> None:
    sync_client.presence("personal:1")


def test_presence_stats(sync_client: Client) -> None:
    sync_client.presence_stats("personal:1")


def test_history(sync_client: Client) -> None:
    sync_client.history(
        channel="personal:1",
        limit=1,
        reverse=True,
    )


def test_history_remove(sync_client: Client) -> None:
    sync_client.history_remove("personal:1")


def test_info(sync_client: Client) -> None:
    sync_client.info()


def test_channels(sync_client: Client) -> None:
    sync_client.channels(
        pattern="*",
    )


def test_disconnect(sync_client: Client) -> None:
    sync_client.disconnect(
        user="user",
        client="client",
        session="session",
        whitelist=["personal:1"],
        disconnect=Disconnect(
            code=4000,
            reason="reason",
        ),
    )


def test_refresh(sync_client: Client) -> None:
    sync_client.refresh(
        user="user",
        client="client",
        session="session",
        expire_at=1,
        expired=True,
    )