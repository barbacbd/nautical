class NauticalError(Exception):
    """
    Exception to be raised during any new error that has occurred in this package.
    """

    def __init__(self, info) -> None:
        """
        :param info: String data passed by the user for more information about the reason
        that this error occurred
        """
        self.info = info
