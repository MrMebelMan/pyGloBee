def remove_empty_keys(self, data: dict = None):
    """ Recursively removes keys with empty values from a dictionary """

    if not data:
        return

    for key, val in dict(data).items():
        if type(val) is dict:
            self.remove_empty_keys(val)
        elif val is None or val == '':
            data.pop(key, None)

