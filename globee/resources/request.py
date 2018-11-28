from requests import get, post
from .result import Result
from .response import GlobeePaymentResponse


class GlobeePingRequest:
    def __init__(self, api_key, endpoint):
        super().__init__()

        headers = {'Accept': 'application/json', 'X-AUTH-KEY': api_key}
        response = get(endpoint + 'ping', headers=headers, verify=True, timeout=5)

        self.status_code = response.status_code
        self.ok = response.ok
        self.reason = response.reason

    def __str__(self):
        return '%d: %s' % (self.status_code, self.reason)


class GlobeePaymentRequest:
    def __init__(self, api_key='', endpoint='', data=None):
        self.response = None

        if not data:
            raise Exception('No data supplied for %s' % self.__class__.__name__)

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-AUTH-KEY': api_key,
        }

        response = post(
            endpoint + 'payment-request',
            headers=headers,
            json=data,
            verify=True,
            timeout=5,
        )

        self.response = GlobeePaymentResponse(response)

    def __str__(self):
        return '%s' % self.response
