from requests import get, post
from .result import Result
from .response import GlobeePaymentResponse


class GlobeeGetRequest(Result):
    def __init__(self, api_key, endpoint):
        super().__init__()

        headers = {
            'Accept': 'application/json',
            'X-AUTH-KEY': api_key,
        }
        
        response = get(
            endpoint,
            headers=headers,
            verify=True,
            timeout=5
        )

        self.status_code = response.status_code
        self.ok = response.ok
        self.reason = response.reason
        self.text = response.text
        self.json = response.json()

    def __str__(self):
        return '%d: %s' % (self.status_code, self.reason)


class GlobeePaymentRequest():
    STATUSES = {
            'unpaid':      'All payment-requests start in the unpaid state, ready to receive payment.',
            'paid':        'The payment request has been paid, waiting for required number of confirmations.',
            'underpaid':   'Payment has been received, however, the user has paid less than the amount requested. '
                           'This generally should not happen, and is only if the user changed the amount during payment.',
            'overpaid':    'Payment has been received, however, the user has mistakenly paid more than the amount requested. '
                           'This generally should not happen, and is only if the user changed the amount during payment.',
            'paid_late':   'Payment has been received, however, the payment was made outside of the quotation window.',
            'confirmed':   'Payment has been confirmed based on your profile confirmation risk settings.',
            'completed':   'The payment-request is now completed, having reached maximum confirmations, and Globee will start its settling process.',
            'refunded':    'The invoice was refunded and cancelled.',
            'cancelled':   'The invoice was cancelled.',
            'draft':       'Invoice has been saved as a draft and not yet active.',
    }

    def __init__(self, api_key='', endpoint='', data=dict()):
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
            timeout=5
        )

        self.response = GlobeePaymentResponse(response)

    def __str__(self):
        return '%s' % self.response

