class Globee404NotFound(Exception):
    def __init__(self):
        super().__init__()
        self.message = 'Payment Request returned 404: Not Found'

    def __str__(self):
        return self.message


class Globee422UnprocessableEntity(Exception):
    def __init__(self, errors):
        super().__init__()
        self.message = 'Payment Request returned 422:'
        self.errors = errors or []

    def __str__(self):
        ret = '%s\n' % self.message
        for error in self.errors:
            ret += '\ttype: %s\n' % error['type']
            ret += '\textra: %s\n' % error['extra']
            ret += '\tfield: %s\n' % error['field']
            ret += '\tmessage: %s\n' % error['message']
        return ret


class GlobeeMissingCredentials(Exception):
    def __init__(self, missing_key_name):
        super().__init__()
        self.message = "The '%s' is missing!" % missing_key_name

    def __str__(self):
        return self.message

