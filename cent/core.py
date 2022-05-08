from typing import Callable, List, Optional

import httpx

from cent import RequestException, ResponseError
from cent.mixins import ParamsMixin


class Client(ParamsMixin):
    """
    Core class to communicate with Centrifugo.
    """

    def __init__(
        self,
        address: str,
        api_key: str = "",
        timeout: int = 1,
        json_encoder: Callable = None,
        session: Callable = None,
        **kwargs
    ):
        """
        :param address: Centrifugo address
        :param api_key: Centrifugo API key
        :param timeout: timeout for HTTP requests to Centrifugo
        :param json_encoder: custom JSON encoder
        :param verify: boolean flag, when set to False no certificate check will be done during requests.
        :param session: custom requests.Session instance
        """

        self.address = address
        self.api_key = api_key
        self.timeout = timeout
        self.json_encoder = json_encoder
        self.session = session or httpx.Client()
        self._prepare_session()
        self.kwargs = kwargs

    def _prepare_session(self):
        self.session.headers["Authorization"] = "apikey " + self.api_key
        self.session.timeout = self.timeout

    def send(self, method, payload):
        payload["method"] = method
        try:
            resp = self.session.post(
                url=self.address,
                json=payload,
                timeout=self.timeout,
            )
        except RequestException as err:
            raise RequestException(err)
        if resp.status_code != 200:
            raise RequestException("wrong status code: %d" % resp.status_code)
        return resp

    def reset(self):
        pass

    def _send_one(self, method: str, payload: dict) -> Optional[dict]:
        resp = self.send(method, payload)
        resp_json = resp.json()
        if "error" in resp_json:
            raise ResponseError(resp_json["error"])
        return resp_json.get("result", {})

    def publish(self, channel: str, data: dict, skip_history: bool = False) -> Optional[dict]:
        result = self._send_one(
            method="publish",
            payload=self.get_publish_params(channel, data, skip_history=skip_history),
        )
        return result

    def broadcast(self, channels: List[str], data: dict, skip_history: bool = False) -> Optional[dict]:
        result = self._send_one(
            method="broadcast",
            payload=self.get_broadcast_params(channels, data, skip_history=skip_history),
        )
        return result

    def subscribe(self, user: str, channel: str, client: Optional[str] = None) -> None:
        self._send_one(
            method="subscribe",
            payload=self.get_subscribe_params(user, channel, client=client),
        )
        return

    def unsubscribe(self, user: str, channel: str, client: Optional[str] = None) -> None:
        self._send_one(
            method="unsubscribe",
            payload=self.get_unsubscribe_params(user, channel, client=client),
        )
        return

    def disconnect(self, user: str, client: Optional[str] = None) -> None:
        self._send_one(
            method="disconnect",
            payload=self.get_disconnect_params(user, client=client),
        )
        return

    def presence(self, channel: str) -> dict:
        result = self._send_one(
            method="presence",
            payload=self.get_presence_params(channel),
        )
        return result["presence"]

    def presence_stats(self, channel: str) -> dict[str, int]:
        result = self._send_one(
            method="presence_stats",
            payload=self.get_presence_stats_params(channel),
        )
        return {
            "num_clients": result["num_clients"],
            "num_users": result["num_users"],
        }

    def history(self, channel: str, limit: int = 0, since: dict = None, reverse: bool = False) -> dict:
        result = self._send_one(
            method="history",
            payload=self.get_history_params(channel, limit=limit, since=since, reverse=reverse),
        )
        return {
            "publications": result.get("publications", []),
            "offset": result.get("offset", 0),
            "epoch": result.get("epoch", ""),
        }

    def history_remove(self, channel: str) -> None:
        self._send_one(
            method="history_remove",
            payload=self.get_history_remove_params(channel),
        )
        return

    def channels(self, pattern="") -> List[Optional[str]]:
        result = self._send_one(
            method="channels",
            payload=self.get_channels_params(pattern=pattern),
        )
        return result["channels"]

    def info(self) -> dict[str, list]:
        result = self._send_one(
            method="info",
            payload=self.get_info_params(),
        )
        return result
