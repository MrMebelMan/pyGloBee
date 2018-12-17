from .result import Result
from json import dumps as json_dumps

from .exceptions import Globee404NotFound, Globee422UnprocessableEntity


class GlobeePaymentResponse(Result):

    def __init__(self, response=None):
        super().__init__()

        self.errors = []
        self.response = response
        self.status_code = response.status_code
        self.reason = response.reason
        self.json = response.json()

        if self.status_code == 404:
            raise Globee404NotFound()
        elif self.status_code == 422:
            self.errors = self.json["errors"]
            raise Globee422UnprocessableEntity(self.errors)
        elif self.status_code != 200 or not self.json["success"]:
            raise Exception("%s: %s" % (self.response, self.reason))


class GlobeeCallbackResponse:
    STATUSES = {
        'unpaid': 'All payment-requests start in the unpaid state, ready to receive payment.',
        'paid': 'The payment request has been paid, waiting for required number of confirmations.',
        'underpaid': 'Payment has been received, however, the user has paid less than the amount requested. '
        'This generally should not happen, and is only if the user changed the amount during payment.',
        'overpaid': 'Payment has been received, however, the user has mistakenly paid more than the amount requested.',
        'paid_late': 'Payment has been received, however, the payment was made outside of the quotation window.',
        'confirmed': 'Payment has been confirmed based on your profile confirmation risk settings.',
        'completed': 'The payment-request is now completed, having reached maximum confirmations, and Globee will start its settling process.',
        'refunded': 'The invoice was refunded and cancelled.',
        'cancelled': 'The invoice was cancelled.',
        'draft': 'Invoice has been saved as a draft and not yet active.',
    }

    def __init__(self, json=None):
        self.json = json
        self.status = json['status']
        self.payment_id = json['id']
        self.custom_payment_id = json['custom_payment_id']
        self.adjusted_total = json['total']
        self.callback_data = json['callback_data']
        self.created_at = json['created_at']
        self.callback_data = json['callback_data']
        self.total = json['total']
        self.adjusted_total = json['adjusted_total']
        self.custom_payment_id = json['custom_payment_id']

        self.customer_name = json['customer']['name']
        self.customer_email = json['customer']['email']

        self.request_currency = json['currency']

        self.payment_currency = json['payment_details']['currency']
        self.received_amount = json['payment_details']['received_amount']
        self.received_difference = json['payment_details']['received_difference']

        self.redirect_url = json['redirect_url']
        self.success_url = json['success_url']
        self.cancel_url = json['cancel_url']
        self.ipn_url = json['ipn_url']

        self.confirmation_speed = json['confirmation_speed']
        self.custom_store_reference = json['custom_store_reference']
    
    def __str__(self):
        return json_dumps(self.json, indent=4, sort_keys=True)

