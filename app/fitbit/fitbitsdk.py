import requests, base64, json
from datetime import datetime
from config import Config

SCOPES = [
    'profile',
    'activity',
    'heartrate',
    'location',
    'nutrition',
    'settings',
    'sleep',
    'social',
    'weight'
]


class Fitbit(object):

    _instance = None

    client_id = ""
    client_secret = ""

    def __init__(self):
        if not self._instance:
            self._instance = super(Fitbit, self).__init__()

        c = Config()
        self.client_id = c.client_id
        self.client_secret = c.client_secret

    def get_permission_screen_url(self):
        print self.client_id
        url = ('https://fitbit.com/oauth2/authorize'
               '?response_type=code&client_id={client_id}&scope={scope}'
               ).format(client_id=self.client_id, scope='%20'.join(SCOPES))
        print url
        return url

    def get_device_info(self, token):
        r = requests.get("https://api.fitbit.com/1/user/-/devices.json",
                         headers={
                            'Authorization': 'Bearer {}'.format(token),
                        }
        )
        r.raise_for_status()
        return r.json()

    def get_heart_data(self, token):
        r = requests.get("https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json",
                         headers={
                             'Authorization': 'Bearer {}'.format(token),
                         }
                         )
        r.raise_for_status()
        return r.json()

    def get_steps_data(self, token):
        r = requests.get("https://api.fitbit.com/1/user/-/activities/steps/date/today/7d.json",
                         headers={
                             'Authorization': 'Bearer {}'.format(token),
                         }
                         )
        r.raise_for_status()
        return r.json()

    def get_activities_data(self, token):
        url = "https://api.fitbit.com/1/user/-/activities/date/{}.json".format(datetime.now().date())
        r = requests.get(url,
                         headers={
                             'Authorization': 'Bearer {}'.format(token),
                         }
                         )
        r.raise_for_status()
        return r.json()

    def get_sleep_data(self, token):
        url = "https://api.fitbit.com/1/user/-/sleep/date/{}.json".format(datetime.now().date())
        r = requests.get(url,
                         headers={
                             'Authorization': 'Bearer {}'.format(token),
                         }
                         )
        r.raise_for_status()
        return r.json()

    def _get_auth_url(self, code):
        return 'https://api.fitbit.com/oauth2/token?code={code}&client_id={client_id}&grant_type=authorization_code'.format(
            code=code,
            client_id=self.client_id
        )

    def do_fitbit_auth(self, code):
        r = requests.post(
            self._get_auth_url(code),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic {}'.format(self._get_token()),
            }
        )
        r.raise_for_status()
        response = r.json()
        return {
            'user_id': response['user_id'],
            'access_token': response['access_token'],
            'refresh_token': response['refresh_token']
        }

    def _get_token(self):
        return base64.b64encode("{}:{}".format(self.client_id, self.client_secret).encode('utf-8')).decode('utf-8')