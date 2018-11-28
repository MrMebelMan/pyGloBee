from .result import Result

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

