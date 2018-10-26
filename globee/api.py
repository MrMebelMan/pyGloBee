from globee.resources.request import (
    GlobeeGetRequest, GlobeePaymentRequest
)


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
        return GlobeeGetRequest(self.api_key, endpoint).ok


    def request_payment(self,
                        total,
                        email,
                        currency           = 'EUR',
                        customer_name      = '',
                        payment_id         = '',
                        store_reference    = '',
                        callback_data      = None,
                        notification_email = '',
                        confirmation_speed = 'medium',
                        success_url        = '',
                        cancel_url         = '',
                        ipn_url            = ''):

        request_data = {
          "total": total,
          "currency": currency,
          "customer": {
              "email": email,
          },
        }

        # Optional
        if payment_id:
            request_data['custom_payment_id'] = payment_id

        if store_reference:
            request_data['custom_store_reference'] = store_reference

        if callback_data:
            request_data['callback_data'] = callback_data

        if notification_email:
            request_data['notification_email'] = notification_email

        if confirmation_speed:
            request_data['confirmation_speed'] = confirmation_speed

        # Recommended
        if customer_name:
            request_data['customer']['name'] = customer_name

        if success_url:
            request_data['success_url'] = success_url

        if cancel_url:
            request_data['cancel_url'] = cancel_url

        if ipn_url:
            request_data['ipn_url'] = ipn_url

        request = GlobeePaymentRequest(
            api_key=self.api_key,
            endpoint=self.api_url,
            data=request_data
        )
        
        return request.response

