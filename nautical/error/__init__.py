class NauticalError(Exception):
    """
    Exception raised as errors occur in the nautical package.
    """

    def __init__(self, message) -> None:
        """
        :param message: Message (string) to the user when the exception is raised.
        """
        super(NauticalError, self).__init__(message)

