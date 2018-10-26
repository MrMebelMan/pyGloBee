from globee.resources.response import GlobeeResponse


class GloBee:

    def __init__(self, api_token, api_secret, testnet=False):
        self.api_token = api_token
        self.api_secret = api_secret

        if testnet:
            self.api_url = 'https://test.globee.com/payment-api/v1/'
        else:
            self.api_url = 'https://globee.com/payment-api/v1/'

