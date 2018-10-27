from .result import Result

from .exceptions import (
    Globee404NotFound, Globee422UnprocessableEntity
)


class GlobeePaymentResponse(Result):
    def __init__(self, response=None):
        super().__init__()

        self.errors = []
        self.status_code = response.status_code
        self.ok = response.ok
        self.reason = response.reason
        self.text = response.text
        self.json = response.json()
        self.redirect_url = ''
        self.payment_id = ''

        if self.status_code == 404:
            raise Globee404NotFound()
        elif self.status_code == 422:
            self.errors = self.json['errors']
            raise Globee422UnprocessableEntity(self.errors)
        elif self.status_code != 200 or not self.json['success']:
            raise ValidationError('%d: %s' % (self.status_code, self.response))

        self.redirect_url = self.json['data']['redirect_url']
        self.payment_id = self.json['data']['id']

