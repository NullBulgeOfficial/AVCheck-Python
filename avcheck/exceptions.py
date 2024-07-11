class AvCheckException(Exception):
    """Base exception class for AvCheckClient."""
    pass

class ApiKeyMissingException(AvCheckException):
    """Raised when the API key is missing."""
    def __init__(self, message="API key is required. Please provide a valid API key."):
        super().__init__(message)

class InvalidResponseException(AvCheckException):
    """Raised when the API response is invalid or contains an error."""
    def __init__(self, status_code, message):
        detailed_message = (
            f"Invalid response {status_code}: {message}\n"
            "This error indicates that the API responded with an unexpected status code. "
            "Please check the following:\n"
            "1. Ensure that your API key is valid and has the necessary permissions.\n"
            "2. Verify that the API endpoint URL is correct.\n"
            "3. Check the API documentation for information on the expected response format."
        )
        super().__init__(detailed_message)
        self.status_code = status_code
        self.message = message

class InvalidInputException(AvCheckException):
    """Raised when the input provided to a method is invalid."""
    def __init__(self, message):
        detailed_message = (
            f"Invalid input: {message}\n"
            "This error indicates that the input provided to a method is invalid. "
            "Please check the following:\n"
            "1. Ensure that all required parameters are provided and are of the correct type.\n"
            "2. Verify that the values of the parameters are within the expected range or format.\n"
            "3. Refer to the API documentation for information on valid input values."
        )
        super().__init__(detailed_message)

class TaskNotFoundException(AvCheckException):
    """Raised when the specified task ID is not found."""
    def __init__(self, task_id):
        detailed_message = (
            f"Task with ID '{task_id}' not found.\n"
            "This error indicates that the specified task ID does not exist or has been deleted. "
            "Please check the following:\n"
            "1. Verify that the task ID is correct and exists in the system.\n"
            "2. Ensure that the task has not expired or been removed.\n"
            "3. If the task ID is correct, try querying the task again after some time."
        )
        super().__init__(detailed_message)
        self.task_id = task_id

class EngineNotFoundException(AvCheckException):
    """Raised when the specified engine is not found in the service info."""
    def __init__(self, engine_name):
        detailed_message = (
            f"Engine '{engine_name}' not found in service info.\n"
            "This error indicates that the specified engine name does not exist in the service information. "
            "Please check the following:\n"
            "1. Verify that the engine name is correct and is included in the service information.\n"
            "2. Ensure that the service information is up-to-date.\n"
            "3. Refer to the API documentation for a list of valid engine names."
        )
        super().__init__(detailed_message)
        self.engine_name = engine_name