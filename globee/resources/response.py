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
