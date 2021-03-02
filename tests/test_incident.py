
import datetime
import pytest

import incident


class IncidentFakeSubmit(incident.Incident):
    json = None

    def _submit(self, json):
        self.json = json

    @staticmethod
    def format_time(time):
        return 'time'  # replace time with something static


def test_simple():
    inc = IncidentFakeSubmit('webhook')

    inc.update(incident.STATE_OUTAGE, 'We got an outage')

    outage = incident.STATE_OUTAGE
    assert inc.json['embeds'][0]['description'] == f'''\
{outage.emoji} **{outage.name}**: We got an outage
*time*\
'''


def test_too_long():
    inc = IncidentFakeSubmit('webhook')
    inc.update(incident.STATE_OUTAGE, 'We got an outage', submit=False)

    for _ in range(100):
        inc.update(incident.STATE_UPDATE, '-' * 20, submit=False)

    assert inc.json is None  # make sure it never submitted

    inc.submit()
    assert len(inc.json['embeds']) > 1


def test_colors():
    inc = IncidentFakeSubmit('webhook')

    with pytest.raises(ValueError, match='no color'):
        inc.update(incident.STATE_UPDATE, 'We got an update')

    inc.update(incident.STATE_OUTAGE, 'We got an outage')
    assert inc.json['embeds'][0]['color'] == incident.STATE_OUTAGE.color

    inc.update(incident.STATE_PARTIAL_OUTAGE, 'We got a partial outage')
    assert inc.json['embeds'][0]['color'] == \
           incident.STATE_PARTIAL_OUTAGE.color

    inc.update(incident.STATE_UPDATE, 'We got an update')
    assert inc.json['embeds'][0]['color'] == \
           incident.STATE_PARTIAL_OUTAGE.color  # update has no color

    inc.update(incident.STATE_RESOLVED, 'Resolved')
    assert inc.json['embeds'][0]['color'] == incident.STATE_RESOLVED.color

    inc.update(incident.STATE_UPDATE, 'We got an update')
    assert inc.json['embeds'][0]['color'] == incident.STATE_RESOLVED.color


def test_title():
    inc = IncidentFakeSubmit('webhook')

    inc.update(incident.STATE_OUTAGE, 'We got an outage')
    assert inc.json['embeds'][0]['title'] == ':hammer_pick: Ongoing incident'

    inc.update(incident.STATE_RESOLVED, 'Resolved')
    assert inc.json['embeds'][0]['title'] == ':hammer_pick: Resolved incident'

    inc.update(incident.STATE_UPDATE, 'We got an update')
    # updates are ignored
    assert inc.json['embeds'][0]['title'] == ':hammer_pick: Resolved incident'

    inc.update(incident.STATE_MAINTENANCE, 'We got a maintenance')
    assert inc.json['embeds'][0]['title'] == ':hammer_pick: Ongoing incident'


def test_default():
    inc = IncidentFakeSubmit('webhook')

    inc.submit()
    noinfo = 'There is an ongoing outage, but no futher information is ' \
             'currently available.'
    assert noinfo in inc.json['embeds'][0]['description']


def test_time():
    t = datetime.datetime.fromisoformat('2021-01-01T00:00:00+00:00')
    assert incident.Incident.format_time(t) == '2021-01-01 00:00:00 (UTC+0000)'

    timezone = datetime.timezone(datetime.timedelta(seconds=7200))  # UTC+2
    t = t.astimezone(timezone)
    assert incident.Incident.format_time(t) == '2021-01-01 02:00:00 (UTC+0200)'
