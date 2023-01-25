from httpx import AsyncClient

from time import time


class ETHAPI:
    BASE_URL: str = "https://mainnet.infura.io/v3/{api_key}"

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

        self._session: AsyncClient = AsyncClient()

    async def get_balance(self, address: str) -> float:
        response_json: dict = (
            await self._session.post(
                url = self.BASE_URL.format(
                    api_key = self.api_key
                ),
                json = {
                    "jsonrpc": "2.0",
                    "method": "eth_getBalance",
                    "params": [
                        address,
                        "latest"
                    ],
                    "id": int(time())
                }
            )
        ).json()

        return int(response_json["result"], 16)
