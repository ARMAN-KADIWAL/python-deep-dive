#!/usr/bin/env python3
"""
Lab 96: Exception Hierarchy with Enhanced Reporting
This script demonstrates exception inheritance and how Python handles exception hierarchies
"""

class ApplicationError(Exception):
    """Base exception class for application-specific errors"""

    def __init__(self, message, error_code=None, context=None):
        self.error_code = error_code
        self.context = context or {}
        super().__init__(message)

    def __str__(self):
        base_message = super().__str__()
        if self.error_code:
            base_message = f"[{self.error_code}] {base_message}"

        if self.context:
            context_info = ", ".join([f"{k}={v}" for k, v in self.context.items()])
            base_message += f" (Context: {context_info})"

        return base_message

class NetworkError(ApplicationError):
    """Network-related errors"""

    def __init__(self, message, host=None, port=None, timeout=None):
        context = {}
        if host:
            context['host'] = host
        if port:
            context['port'] = port
        if timeout:
            context['timeout'] = timeout

        super().__init__(message, "NET_ERROR", context)

class APIError(NetworkError):
    """API-specific network errors"""

    def __init__(self, message, endpoint=None, status_code=None, response_body=None):
        context = {}
        if endpoint:
            context['endpoint'] = endpoint
        if status_code:
            context['status_code'] = status_code
        if response_body:
            context['response_body'] = response_body[:100]  # Truncate long responses

        super().__init__(message, endpoint, 443)  # HTTPS port
        self.error_code = "API_ERROR"
        self.context.update(context)

class DataError(ApplicationError):
    """Data processing errors"""

    def __init__(self, message, data_source=None, record_id=None, field_name=None):
        context = {}
        if data_source:
            context['data_source'] = data_source
        if record_id:
            context['record_id'] = record_id
        if field_name:
            context['field_name'] = field_name

        super().__init__(message, "DATA_ERROR", context)

class ValidationError(DataError):
    """Data validation specific errors"""

    def __init__(self, message, field_name, expected_type=None, actual_value=None):
        context = {
            'field_name': field_name,
            'expected_type': expected_type.__name__ if expected_type else 'unknown',
            'actual_type': type(actual_value).__name__ if actual_value is not None else 'None',
            'actual_value': str(actual_value)[:50] if actual_value is not None else 'None'
        }

        super().__init__(message, field_name=field_name)
        self.error_code = "VALIDATION_ERROR"
        self.context.update(context)

def demonstrate_exception_hierarchy():
    """Demonstrate exception hierarchy and catching"""
    print("=== Exception Hierarchy Demonstration ===")

    def simulate_api_call(endpoint, data):
        """Simulate API call that can fail in various ways"""
        if endpoint == "/invalid":
            raise APIError("Invalid endpoint",
                          endpoint=endpoint,
                          status_code=404,
                          response_body="Not Found")

        if not isinstance(data, dict):
            raise ValidationError(
                "Invalid payload", "data", dict, data
            )

        if endpoint == "/timeout":
            raise NetworkError("Connection timed out", host="example.com", timeout=5)

        if "user_id" not in data:
            raise DataError("Missing user ID", field_name="user_id")

        return {"status": "success", "data": data}

    cases = [
        ("/invalid", {}),
        ("/users", "invalid"),
        ("/timeout", {}),
        ("/users", {}),
        ("/users", {"user_id": 1})
    ]

    for endpoint, data in cases:
        try:
            print(simulate_api_call(endpoint, data))
        except APIError as e:
            print("APIError:", e)
        except ValidationError as e:
            print("ValidationError:", e)
        except NetworkError as e:
            print("NetworkError:", e)
        except DataError as e:
            print("DataError:", e)
        except ApplicationError as e:
            print("ApplicationError:", e)

    assert issubclass(APIError, NetworkError)
    assert issubclass(ValidationError, DataError)
    assert issubclass(NetworkError, ApplicationError)
    assert issubclass(DataError, ApplicationError)
    print("Exception hierarchy verified!")


if __name__ == "__main__":
    demonstrate_exception_hierarchy()
