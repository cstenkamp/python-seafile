import requests
from seafileapi.utils import urljoin
from seafileapi.exceptions import ClientHttpError
from seafileapi.repos import Repos

class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SeafileApiClient(object):
    """Wraps seafile web api"""
    def __init__(self, server, username=None, password=None, token=None, debug=False):
        """Wraps various basic operations to interact with seahub http api.
        """
        self.server = server
        self.username = username
        self.password = password
        self._token = token
        self.debug = debug

        self.repos = Repos(self)
        self.groups = Groups(self)

        if token is None:
            self._get_token()

    def _get_token(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        url = urljoin(self.server, '/api2/auth-token/')
        if self.debug:
            print(f'{c.FAIL}REQUEST: %s %s{c.END}' % (url, data))
        res = requests.post(url, data=data)
        if self.debug:
            print(f'{c.OKBLUE}REPLY:   %s{c.END}' % res.content)
            print('-' * 120)
        if res.status_code != 200:
            raise ClientHttpError(res.status_code, res.content)
        token = res.json()['token']
        assert len(token) == 40, 'The length of seahub api auth token should be 40'
        self._token = token

    def __str__(self):
        return 'SeafileApiClient[server=%s, user=%s]' % (self.server, self.username)

    __repr__ = __str__

    def get(self, *args, **kwargs):
        return self._send_request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._send_request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._send_request('PUT', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._send_request('delete', *args, **kwargs)

    def _send_request(self, method, url, *args, **kwargs):
        if not url.startswith('http'):
            url = urljoin(self.server, url)

        if not '/seafhttp/' in url:
            headers = kwargs.get('headers', {})
            headers.setdefault('Authorization', 'Token ' + self._token)
            kwargs['headers'] = headers

        expected = kwargs.pop('expected', 200)
        if not hasattr(expected, '__iter__'):
            expected = (expected, )
        if self.debug:
            print(f'{c.HEADER}REQUEST: %s %s %s %s{c.END}' % (method, url, args, kwargs))
        resp = requests.request(method, url, *args, **kwargs)
        if self.debug:
            if resp.request.method == 'POST':
                print(f'{c.WARN+c.BOLD}POSTBODY: %s{c.END}' % resp.request.body)
            print(f'{c.OKGREEN}REPLY:   %s{c.END}' % resp.content)
            print('-' * 120)
        if resp.status_code not in expected:
            msg = 'Expected %s, but get %s' % \
                  (' or '.join(map(str, expected)), resp.status_code)
            raise ClientHttpError(resp.status_code, msg)

        return resp


class Groups(object):
    def __init__(self, client):
        pass

    def create_group(self, name):
        pass
