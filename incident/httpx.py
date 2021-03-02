
import httpx

from .incident import Incident


class HttpxIncident(Incident):
    def __init__(self, webhook: str, client: httpx.Client = None):
        super().__init__(webhook)
        self.client = client

    def _submit(self, json):
        if self.client is None:
            with httpx.Client() as client:
                self._submit2(json, client)
        else:
            self._submit2(json, self.client)

    def _submit2(self, json, client: httpx.Client):
        if self.message_id is None:
            message = client.post(f'{self.webhook}?wait=true', json=json)
            self.message_id = message.json()['id']
        else:
            client.patch(
                f'{self.webhook}/messages/{self.message_id}', json=json
            )


class HttpxAsyncIncident(Incident):
    def __init__(self, webhook: str, client: httpx.AsyncClient = None):
        super().__init__(webhook)
        self.client = client

    async def _submit(self, json):
        if self.client is None:
            async with httpx.AsyncClient() as client:
                await self._submit2(json, client)
        else:
            await self._submit2(json, self.client)

    async def _submit2(self, json, client: httpx.AsyncClient):
        if self.message_id is None:
            message = await client.post(f'{self.webhook}?wait=true', json=json)
            self.message_id = message.json()['id']
        else:
            await client.patch(
                f'{self.webhook}/messages/{self.message_id}', json=json
            )
