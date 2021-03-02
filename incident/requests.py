
import requests

from .incident import Incident


class RequestsIncident(Incident):
    def __init__(self, webhook: str, session: requests.Session = None):
        super().__init__(webhook)
        self.session = session

    def _submit(self, json):
        if self.session is None:
            with requests.Session() as session:
                self._submit2(json, session)
        else:
            self._submit2(json, self.session)

    def _submit2(self, json, session: requests.Session):
        if self.message_id is None:
            message = session.post(f'{self.webhook}?wait=true', json=json)
            self.message_id = message.json()['id']
        else:
            session.patch(
                f'{self.webhook}/messages/{self.message_id}', json=json
            )
