class Result():
    def __init__(self):
        self.status_code = 0
        self.ok = False
        self.reason = ''
        self.json = {}
        self.text = ''
        self.exception = None

    def __str__(self):
        return '%d: %s\n%s' % (self.status_code, self.reason, self.json)
