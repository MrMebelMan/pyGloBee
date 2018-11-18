from django.core.exceptions import ValidationError

from .resources.request import GlobeePingRequest, GlobeePaymentRequest
from .resources.utils import remove_empty_keys
from .resources.exceptions import GlobeeMissingCredentials, GlobeePaymentError
from json import dumps as json_dumps
from decimal import Decimal


class GlobeePayment:
    STATUSES = {
        'unpaid': 'All payment-requests start in the unpaid state, ready to receive payment.',
        'paid': 'The payment request has been paid, waiting for required number of confirmations.',
        'underpaid': 'Payment has been received, however, the user has paid less than the amount requested. '
        'This generally should not happen, and is only if the user changed the amount during payment.',
        'overpaid': 'Payment has been received, however, the user has mistakenly paid more than the amount requested. '
        'This generally should not happen, and is only if the user changed the amount during payment.',
        'paid_late': 'Payment has been received, however, the payment was made outside of the quotation window.',
        'confirmed': 'Payment has been confirmed based on your profile confirmation risk settings.',
        'completed': 'The payment-request is now completed, having reached maximum confirmations,\
                      and Globee will start its settling process.',
        'refunded': 'The invoice was refunded and cancelled.',
        'cancelled': 'The invoice was cancelled.',
        'draft': 'Invoice has been saved as a draft and not yet active.',
    }

    def __init__(self, json):
        try:
            self.json = json['data']
            self.callback_data          = self.json['adjusted_total']
            self.callback_data          = self.json['callback_data']
            self.cancel_url             = self.json['cancel_url']
            self.confirmation_speed     = self.json['confirmation_speed']
            self.created_at             = self.json['created_at']
            self.currency               = self.json['currency']
            self.custom_payment_id      = self.json['custom_payment_id']
            self.custom_store_reference = self.json['custom_store_reference']
            self.expires_at             = self.json['expires_at']
            self.id                     = self.json['id']
            self.ipn_url                = self.json['ipn_url']
            self.notification_email     = self.json['notification_email']
            self.redirect_url           = self.json['redirect_url']
            self.status                 = self.json['status']
            self.success_url            = self.json['success_url']
            self.total                  = Decimal(self.json['total'])
            self.customer_name          = self.json['customer']['name']
            self.customer_email         = self.json['customer']['email']
            self.payment_currency       = self.json['payment_details']['currency']
            self.received_amount        = Decimal(self.json['payment_details']['received_amount'] or '0')
            self.received_difference    = Decimal(self.json['payment_details']['received_difference'] or '0')
        except KeyError as e:
            raise GlobeePaymentError(e)

    def __str__(self):
        return 'GloBee Payment #%s (%.2f %s), created: %s, status: %s' \
               % (self.id, self.total, self.currency, self.created_at, self.status)

    @property
    def json_pretty(self):
        return json_dumps(self.json, indent=4, sort_keys=True)


class Globee:
    def __init__(self, api_key, api_secret, testnet=True):
        if not api_key:
            raise GlobeeMissingCredentials('api_key')
        ## api_secret is reserved for future use, not active yet
        # elif not api_secret:
        #     raise GlobeeMissingCredentials('api_secret')

        self.api_key = api_key
        self.api_secret = api_secret

        if testnet:
            self.api_url = 'https://test.globee.com/payment-api/v1/'
        else:
            self.api_url = 'https://globee.com/payment-api/v1/'

    @property
    def available(self):
        return GlobeePingRequest(self.api_key, self.api_url).ok

    def request_payment(
        self,
        total,
        email,
        currency='EUR',
        customer_name='',
        payment_id='',
        store_reference='',
        callback_data=None,
        notification_email='',
        confirmation_speed='medium',
        success_url='',
        cancel_url='',
        ipn_url='',
    ):

        customer_data = {
            'email': email,
            'name': customer_name,
        }

        request_data = {
            'total': float(total),
            'currency': currency,
            'customer': customer_data,
            'custom_payment_id': payment_id,
            'custom_store_reference': store_reference,
            'callback_data': callback_data,
            'notification_email': notification_email,
            'confirmation_speed': confirmation_speed,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'ipn_url': ipn_url,
        }

        remove_empty_keys(request_data)

        request = GlobeePaymentRequest(
            api_key=self.api_key,
            endpoint=self.api_url,
            data=request_data
        )
        return GlobeePayment(request.response.json)

