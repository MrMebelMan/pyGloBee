from globee.resources.request import GlobeeRequest


class Globee:

    def __init__(self, api_key, api_secret, testnet=False):
        self.api_key = api_key
        self.api_secret = api_secret

        if testnet:
            self.api_url = 'https://test.globee.com/payment-api/v1/'
        else:
            self.api_url = 'https://globee.com/payment-api/v1/'

    @property
    def available(self):
        endpoint = self.api_url + 'ping'
        return GlobeeRequest(self.api_key, endpoint).ok
