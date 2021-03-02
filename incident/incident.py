
from collections import namedtuple
import datetime
import typing as t


State = namedtuple('State', ('name', 'emoji', 'color'))
Update = namedtuple('Update', ('state', 'message', 'when'))

STATE_OUTAGE = State('Outage', '<:outage:812640646937706547>', 0xff0000)
STATE_PARTIAL_OUTAGE = State('Partial Outage', '<:partial:812640663539679302>',
                             0xfaa61a)
STATE_MAINTENANCE = State('Maintenance', '<:partial:812640663539679302>',
                          0xfaa61a)
STATE_UPDATE = State('Update', ':memo:', None)
STATE_RESOLVED = State('Resolved', '<:resolved:812640676701143050>', 0x00ff00)


class Incident:
    updates: t.List[Update]

    def __init__(self, webhook: str):
        self.webhook = webhook
        self.updates = []
        self.message_id = None

    def update(self, state: State, message: str,
               when: datetime.datetime = None, submit: bool = True):
        if when is None:
            when = datetime.datetime.utcnow()
        self.updates.append(Update(state, message, when))
        if submit:
            return self.submit()

    def submit(self):
        updates = self.updates
        if not updates:
            updates = [Update(
                STATE_PARTIAL_OUTAGE,
                'There is an ongoing outage, but no futher information is '
                'currently available.',
                datetime.datetime.utcnow()
            )]

        message = '\n\n'.join(
            f'{x.state.emoji} **{x.state.name}**: {x.message}\n'
            f'*{self.format_time(x.when)}*'
            for x in updates
        )

        for update in reversed(updates):
            if update.state.color is not None:
                break
        else:
            # this only happens when the only update is a STATE_UPDATE
            raise ValueError('no color')

        json = {
            'embeds': [
                {
                    'description': '',
                    'color': update.state.color
                }
            ]
        }
        for line in message.splitlines(keepends=True):
            if len(json['embeds'][-1]['description']) + len(line) >= 2000:
                json['embeds'].append({
                    'description': '',
                    'color': update.state.color
                })
            json['embeds'][-1]['description'] += line

        json['embeds'][0]['title'] = ':hammer_pick: ' + (
            'Resolved incident' if update.state == STATE_RESOLVED else
            'Ongoing incident'
        )

        return self._submit(json)

    def _submit(self, json):
        raise NotImplementedError

    @staticmethod
    def format_time(time):
        return time.strftime('%Y-%m-%d %H:%M:%S (UTC%z)')
