from globee.resources.request import GlobeeGetRequest, GlobeePaymentRequest
from globee.resources.utils import remove_empty_keys
from globee.resources.exceptions import GlobeeMissingCredentials


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
        endpoint = self.api_url + "ping"
        return GlobeeGetRequest(self.api_key, endpoint).ok

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

        return request.response
