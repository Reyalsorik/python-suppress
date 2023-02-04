#!/usr/bin/env python3

"""Contains the logic for suppressing and logging exceptions after an expected exception/result is captured."""

import logging
from typing import Type, Any


class Suppress(object):
    """Decorator for suppressing and logging exceptions after an expected exception/result is captured."""

    def __init__(self, exception_type: Type[BaseException], exception_message: str, logger_name: str = None) -> None:
        """Initialize.

        :param exception_type: type of exception
        :param exception_message: message in an exception to suppress
        """
        self.exception_type = exception_type
        self.exception_message = exception_message
        self.logger = logging.getLogger(logger_name)
        self.function = None

    def __call__(self, function: Any, *args, **kwargs) -> Any:
        """Callable.

        :param function: function to suppress exceptions
        """
        self.function = function
        if self.function is None:
            raise TypeError(f"{self.__class__.__name__} takes 0 positional arguments but 1 was given, did you mean 'Suppress()'?")  # Decorator must be called

        def suppress_wrapper(*wrapped_args, **wrapped_kwargs):
            """Wrap the function and suppress expected exceptions."""
            try:
                return function(*wrapped_args, **wrapped_kwargs)
            except self.exception_type as exception:
                if self.exception_message not in str(exception) + getattr(exception, "stdout", str()):
                    raise
                self.logger.debug(f"Suppressing expected exception; '{self.exception_message}' found in '{getattr(exception, 'stdout', str()) or exception}'.")
                return dict()
        return suppress_wrapper
