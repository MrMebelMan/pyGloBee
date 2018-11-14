from .result import Result

from .exceptions import Globee404NotFound, Globee422UnprocessableEntity


class GlobeePaymentResponse(Result):
    STATUSES = {
        "unpaid": "All payment-requests start in the unpaid state, ready to receive payment.",
        "paid": "The payment request has been paid, waiting for required number of confirmations.",
        "underpaid": "Payment has been received, however, the user has paid less than the amount requested. "
        "This generally should not happen, and is only if the user changed the amount during payment.",
        "overpaid": "Payment has been received, however, the user has mistakenly paid more than the amount requested. "
        "This generally should not happen, and is only if the user changed the amount during payment.",
        "paid_late": "Payment has been received, however, the payment was made outside of the quotation window.",
        "confirmed": "Payment has been confirmed based on your profile confirmation risk settings.",
        "completed": "The payment-request is now completed, having reached maximum confirmations, and Globee will start its settling process.",
        "refunded": "The invoice was refunded and cancelled.",
        "cancelled": "The invoice was cancelled.",
        "draft": "Invoice has been saved as a draft and not yet active.",
    }

    def __init__(self, response=None):
        super().__init__()

        self.errors = []
        self.response = response
        self.status_code = response.status_code
        self.ok = response.ok
        self.reason = response.reason
        self.text = response.text
        self.json = response.json()
        self.redirect_url = ""
        self.payment_id = ""

        if self.status_code == 404:
            raise Globee404NotFound()
        elif self.status_code == 422:
            self.errors = self.json["errors"]
            raise Globee422UnprocessableEntity(self.errors)
        elif self.status_code != 200 or not self.json["success"]:
            raise Exception("%s: %s" % (self.response, self.reason))

        self.redirect_url = self.json["data"]["redirect_url"]
        self.payment_id = self.json["data"]["id"]
