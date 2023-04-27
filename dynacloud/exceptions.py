class CustomException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        self.name = self.__class__.__name__

    def __str__(self):
        return self.message

