# Create file: exception_logger.py
import logging
import traceback
import sys
import functools
from datetime import datetime
from custom_formatters import JSONFormatter

class ExceptionLogger:
    """Advanced exception logging with detailed stack traces"""
    
    def __init__(self, logger_name='exception_logger'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Set up handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up logging handlers for exception logging"""
        
        # File handler for exceptions
        exception_handler = logging.FileHandler('exception_logs.log', encoding='utf-8')
        exception_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        exception_handler.setFormatter(exception_formatter)
        self.logger.addHandler(exception_handler)
        
        # JSON handler for structured exception data
        json_handler = logging.FileHandler('exception_logs.json', encoding='utf-8')
        json_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(json_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(levelname)s: %(message)s'
        ))
        self.logger.addHandler(console_handler)
    
    def log_exception(self, exc_info=None, context=None):
        """Log exception with detailed information"""
        if exc_info is None:
            exc_info = sys.exc_info()
        
        exc_type, exc_value, exc_traceback = exc_info
        
        if exc_type is None:
            self.logger.warning("log_exception called but no exception is active")
            return
        
        # Create detailed exception information
        exception_details = {
            'exception_type': exc_type.__name__,
            'exception_message': str(exc_value),
            'traceback': traceback.format_exception(exc_type, exc_value, exc_traceback),
            'context': context or {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Log the exception
        self.logger.error(
            f"Exception occurred: {exc_type.__name__}: {exc_value}",
            exc_info=exc_info,
            extra={'exception_details': exception_details}
        )
    
    def exception_decorator(self, reraise=True, context=None):
        """Decorator to automatically log exceptions in functions"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    func_context = {
                        'function': func.__name__,
                        'args': str(args)[:200],  # Limit length
                        'kwargs': str(kwargs)[:200],
                        'custom_context': context
                    }
                    self.log_exception(context=func_context)
                    if reraise:
                        raise
                    return None
            return wrapper
        return decorator

# Global exception logger instance
exception_logger = ExceptionLogger()

def setup_global_exception_handler():
    """Set up global exception handler for uncaught exceptions"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Allow KeyboardInterrupt to work normally
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        exception_logger.log_exception((exc_type, exc_value, exc_traceback), 
                                     context={'source': 'global_handler'})
    
    sys.excepthook = handle_exception
