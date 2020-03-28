class NauticalError(Exception):
    """
    Exception to be raised during any new error that has occurred in this package.
    """

    def __init__(self, message) -> None:
        """
        :param message: String data passed by the user for more information about the reason
        that this error occurred
        """
        super(NauticalError, self).__init__(message)
