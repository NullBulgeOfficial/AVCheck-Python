class AvCheckException(Exception):
    """Base exception class for AvCheckClient."""
    pass

class ApiKeyMissingException(AvCheckException):
    """Raised when the API key is missing."""
    pass

class InvalidResponseException(AvCheckException):
    """Raised when the API response is invalid or contains an error."""
    def __init__(self, status_code, message):
        super().__init__(f"Invalid response {status_code}: {message}")
        self.status_code = status_code
        self.message = message