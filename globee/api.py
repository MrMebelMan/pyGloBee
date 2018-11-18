from globee.resources.request import GlobeePingRequest, GlobeePaymentRequest
from globee.resources.utils import remove_empty_keys
from globee.resources.exceptions import GlobeeMissingCredentials
from decimal import Decimal


class GlobeePayment:
    STATUSES = {
        "unpaid": "All payment-requests start in the unpaid state, ready to receive payment.",
        "paid": "The payment request has been paid, waiting for required number of confirmations.",
        "underpaid": "Payment has been received, however, the user has paid less than the amount requested. "
        "This generally should not happen, and is only if the user changed the amount during payment.",
        "overpaid": "Payment has been received, however, the user has mistakenly paid more than the amount requested. "
        "This generally should not happen, and is only if the user changed the amount during payment.",
        "paid_late": "Payment has been received, however, the payment was made outside of the quotation window.",
        "confirmed": "Payment has been confirmed based on your profile confirmation risk settings.",
        "completed": "The payment-request is now completed, having reached maximum confirmations,\
                      and Globee will start its settling process.",
        "refunded": "The invoice was refunded and cancelled.",
        "cancelled": "The invoice was cancelled.",
        "draft": "Invoice has been saved as a draft and not yet active.",
    }

    def __init__(self, json):
        self.success = json['success']
        data = json['data']
        
        self.adjusted_total = data["adjusted_total"]
        self.callback_data = data["callback_data"]
        self.cancel_url = data["cancel_url"]
        self.confirmation_speed = data["confirmation_speed"]
        self.created_at = data["created_at"]
        self.currency = data["currency"]
        self.custom_payment_id = data["custom_payment_id"]
        self.custom_store_reference = data["custom_store_reference"]
        self.expires_at = data["expires_at"]
        self.id = data["id"]
        self.ipn_url = data["ipn_url"]
        self.notification_email = data["notification_email"]
        self.redirect_url = data["redirect_url"]
        self.status = data["status"]
        self.success_url = data["success_url"]
        self.total = Decimal(data["total"])
        
        self.customer_name = data['customer']['name']
        self.customer_email = data['customer']['email']
        
        self.payment_currency = data['payment_details']['currency']
        self.received_amount = Decimal(data['payment_details']['received_amount'] or '0')
        self.received_difference = Decimal(data['payment_details']['received_difference'] or '0')

    def __str__(self):
        return "GloBee Payment #%s (%.2f %s), created: %s, status: %s" \
               % (self.id, self.total, self.currency, self.created_at, self.status)


class Globee:
    def __init__(self, api_key, api_secret, testnet=True):
        if not api_key:
            raise GlobeeMissingCredentials('api_key')
        elif not api_secret:
            raise GlobeeMissingCredentials('api_secret')

        self.api_key = api_key
        self.api_secret = api_secret

        if testnet:
            self.api_url = "https://test.globee.com/payment-api/v1/"
        else:
            self.api_url = "https://globee.com/payment-api/v1/"

    @property
    def available(self):
        return GlobeePingRequest(self.api_key, self.api_url).ok

    def request_payment(
        self,
        total,
        email,
        currency="EUR",
        customer_name="",
        payment_id="",
        store_reference="",
        callback_data=None,
        notification_email="",
        confirmation_speed="medium",
        success_url="",
        cancel_url="",
        ipn_url="",
    ):

        customer_data = {
            "email": email,
            "name": customer_name,
        }

        request_data = {
            "total": float(total),
            "currency": currency,
            "customer": customer_data,
            "custom_payment_id": payment_id,
            "custom_store_reference": store_reference,
            "callback_data": callback_data,
            "notification_email": notification_email,
            "confirmation_speed": confirmation_speed,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "ipn_url": ipn_url,
        }

        remove_empty_keys(request_data)

        request = GlobeePaymentRequest(
            api_key=self.api_key,
            endpoint=self.api_url,
            data=request_data
        )
        return GlobeePayment(request.response.json)

