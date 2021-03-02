
import aiohttp

from .incident import Incident


class AiohttpIncident(Incident):
    def __init__(self, webhook: str,
                 session: aiohttp.ClientSession = None):
        super().__init__(webhook)
        self.session = session

    async def _submit(self, json):
        if self.session is None:
            async with aiohttp.ClientSession() as session:
                await self._submit2(json, session)
        else:
            await self._submit2(json, self.session)

    async def _submit2(self, json, session: aiohttp.ClientSession):
        if self.message_id is None:
            async with session.post(f'{self.webhook}?wait=true', json=json) \
                    as resp:
                self.message_id = (await resp.json())['id']
        else:
            await session.patch(
                f'{self.webhook}/messages/{self.message_id}', json=json
            )
