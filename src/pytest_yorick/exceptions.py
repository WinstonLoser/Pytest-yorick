class YamlException(Exception):
    """Custom exception for error reporting."""

    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class YamlFileError(Exception):
    """YamlFile Error"""


class YamlItemError(Exception):
    """YamlItem Error"""


class BadSchemaError(Exception):
    """Schema mismatch"""


class JSONComparisonError(Exception):
    """Base class for exceptions in this module."""
    pass


class MissingKeyError(JSONComparisonError):
    """Exception raised for missing key in JSON comparison."""

    def __init__(self, key, path):
        self.key = key
        self.path = path
        self.message = f"Missing key '{self.path}{self.key}' in actual response."
        super().__init__(self.message)


class LengthMismatchError(JSONComparisonError):
    """Exception raised for length mismatch in lists."""

    def __init__(self, expected_length, actual_length, path):
        self.expected_length = expected_length
        self.actual_length = actual_length
        self.path = path
        self.message = f"List length mismatch at '{self.path}': expected {self.expected_length}, got {self.actual_length}"
        super().__init__(self.message)


class ValueMismatchError(JSONComparisonError):
    """Exception raised for value mismatch in JSON comparison."""

    def __init__(self, expected_value, actual_value, path):
        self.expected_value = expected_value
        self.actual_value = actual_value
        self.path = path
        self.message = f"Value mismatch at '{self.path}': expected '{self.expected_value}', got '{self.actual_value}'"
        super().__init__(self.message)


class StatusCodeMismatchError(Exception):
    def __init__(self, expected_statuscode, actual_statuscode):
        message = f"StatusCode mismatch: expected '{expected_statuscode}', got '{actual_statuscode}'"
        super().__init__(message)


class RequestError(Exception):
    def __init__(self, message):
        super().__init__(message)


class CompileError(Exception):
    def __init__(self, message):
        super().__init__(message)
