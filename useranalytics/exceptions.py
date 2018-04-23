class CustomException(Exception):
    """
    Custom Exception for blended raise when something specific goes wrong.
    """
    def __init_(self, message, status_code, *args):
        self.status_code = status_code
        super(CustomException, self).__init__(message, status_code, *args)