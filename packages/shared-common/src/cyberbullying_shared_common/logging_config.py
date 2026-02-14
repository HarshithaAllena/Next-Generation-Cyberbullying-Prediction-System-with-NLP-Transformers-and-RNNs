# =============================================================================
# LOGGING CONFIGURATION MODULE
# =============================================================================
# Purpose: Provides centralized logging setup for all microservices.
# This module ensures consistent logging across the entire application.
#
# Key Features:
# - Structured logging with structlog
# - JSON output for log aggregation
# - Different log levels per environment
# - Request ID tracking
# - Exception logging with stack traces
#
# Usage:
#     from cyberbullying_shared_common import setup_logging, get_logger
#     
#     # Initialize logging (call once at app startup)
#     setup_logging()
#     
#     # Get logger for module
#     logger = get_logger(__name__)
#     logger.info("message", key="value")
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
# Standard library imports for system operations
import sys  # Access to system-specific parameters
import os  # Operating system interface
import logging  # Logging facility for Python
from typing import Any, Dict, Optional  # Type hints for better IDE support

# Third-party imports for structured logging
import structlog  # Structured logging library
from structlog.stdlib import (
    LoggerFactory,
    add_log_level,
    add_logger_name,
)  # Structlog processors
from structlog.processors import (
    TimeStamper,  # Add timestamps to log entries
    StackInfoRenderer,  # Add stack information
    format_exc_info,  # Format exception information
    UnicodeDecoder,  # Handle Unicode encoding
    JSONRenderer,  # Render logs as JSON
)

# =============================================================================
# CONSTANTS
# =============================================================================

# Log level environment variable name
# Used to set log level from environment
ENV_LOG_LEVEL = "LOG_LEVEL"

# Default log level if not specified in environment
# INFO is a good default for production (not too verbose)
DEFAULT_LOG_LEVEL = "INFO"

# Log format options
LOG_FORMAT_JSON = "json"
LOG_FORMAT_CONSOLE = "console"

# =============================================================================
# LOG LEVEL MAPPING
# =============================================================================
# Maps string log levels to Python logging constants
# This allows environment variables to set log levels dynamically

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,    # Detailed information for debugging
    "INFO": logging.INFO,      # Confirmation that things work as expected
    "WARNING": logging.WARNING,  # Something unexpected, but not critical
    "ERROR": logging.ERROR,    # Serious problem, function couldn't execute
    "CRITICAL": logging.CRITICAL,  # Very serious error, program may crash
}

# =============================================================================
# STRUCTLOG CONFIGURATION
# =============================================================================

def configure_structlog(
    log_level: str = DEFAULT_LOG_LEVEL,
    log_format: str = LOG_FORMAT_JSON,
) -> None:
    """
    Configure structlog with processors and renderers.
    
    This function sets up the complete logging pipeline:
    1. Capture log calls (INFO, WARNING, ERROR, etc.)
    2. Add contextual information (timestamp, level, logger name)
    3. Handle exceptions (format stack traces)
    4. Render output (JSON or console)
    
    Args:
        log_level: The minimum log level to capture
                   Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        log_format: Output format - "json" or "console"
                   JSON is recommended for production/log aggregation
                   Console is better for development/debugging
    
    Returns:
        None - Configures logging in-place
    
    Example:
        # Development setup with console output
        configure_structlog(log_level="DEBUG", log_format="console")
        
        # Production setup with JSON output
        configure_structlog(log_level="INFO", log_format="json")
    """
    
    # Get the numeric log level from string
    # Defaults to INFO if invalid level specified
    level = LOG_LEVELS.get(log_level.upper(), logging.INFO)
    
    # =================================================================
    # PROCESSORS - Chain of transformations applied to log entries
    # =================================================================
    # Each processor adds or modifies log entry data
    # Order matters - processors are applied in sequence
    
    # Processor 1: Add timestamp to all log entries
    # fmt="iso" creates ISO 8601 format timestamps
    # This is important for log aggregation and analysis
    processors = [
        # Add timestamp in ISO 8601 format
        # Example: "2024-01-15T10:30:00.123456Z"
        TimeStamper(fmt="iso", utc=True),
        
        # Add the logger name to each log entry
        # Helps identify which module generated the log
        add_logger_name,
        
        # Add log level (INFO, WARNING, ERROR, etc.)
        # Essential for filtering and searching logs
        add_log_level,
        
        # Add stack information if available
        # Useful for debugging, shows call stack
        StackInfoRenderer(),
        
        # Format exception information if present
        # Converts Python exceptions to readable strings
        # Includes traceback, line numbers, etc.
        format_exc_info,
        
        # Decode Unicode to handle special characters
        # Ensures logs don't break on non-ASCII text
        UnicodeDecoder(),
    ]
    
    # =================================================================
    # RENDERER - How to output the final log entry
    # =================================================================
    # After all processors, renderer determines output format
    
    if log_format == LOG_FORMAT_JSON:
        # JSON output for production and log aggregation
        # Compatible with ELK stack, Splunk, CloudWatch, etc.
        # Each log line is a valid JSON object
        processors.append(
            JSONRenderer(
                # Ensure datetime objects are serialized properly
                # default=str converts non-JSON types to strings
                default=str,
            )
        )
    else:
        # Console output for development
        # Human-readable format with colors
        # Best for debugging during development
        from structlog.dev import ConsoleRenderer
        
        processors.append(
            ConsoleRenderer(
                # Use colors for different log levels
                # Makes it easy to spot errors in console
                colors=True,
            )
        )
    
    # =================================================================
    # CONFIGURE STANDARD LIBRARY LOGGING
    # =================================================================
    # We use structlog but need to integrate with Python's logging
    
    # Configure logging handler
    # This intercepts standard logging calls and routes to structlog
    logging.basicConfig(
        format="%(message)s",  # Message only, structlog handles the rest
        stream=sys.stdout,     # Output to stdout (Docker-friendly)
        level=level,           # Set minimum log level
    )
    
    # Configure structlog
    # This is the main configuration call
    structlog.configure(
        processors=processors,          # Our processor chain
        wrapper_class=structlog.make_filtering_bound_logger(level),
        # Use filtering bound logger for level control
        context_class=dict,              # Log context as Python dict
        logger_factory=LoggerFactory(),  # Factory for creating loggers
        cache_logger_on_first_use=True,  # Performance optimization
        # Cache logger to avoid recreating for each log call
    )


def setup_logging(
    log_level: Optional[str] = None,
    log_format: Optional[str] = None,
) -> None:
    """
    Main entry point for logging setup.
    
    This function should be called once at application startup
    to initialize logging for all services.
    
    Args:
        log_level: Log level from environment or config
                   If None, reads from LOG_LEVEL environment variable
                   If not set, defaults to "INFO"
        log_format: Output format - "json" or "console"
                    If None, uses "json" in production, "console" in dev
    
    Returns:
        None - Configures logging in-place
    
    Example:
        # Simple setup with defaults
        setup_logging()
        
        # Custom configuration
        setup_logging(log_level="DEBUG", log_format="console")
    """
    
    # Determine log level
    # Priority: 1) parameter, 2) environment variable, 3) default
    if log_level is None:
        # Read from environment variable
        # This allows changing log level without code changes
        log_level = os.environ.get(ENV_LOG_LEVEL, DEFAULT_LOG_LEVEL)
    
    # Determine log format
    # Priority: 1) parameter, 2) environment (LOG_FORMAT), 3) auto-detect
    if log_format is None:
        # Check environment variable
        log_format = os.environ.get("LOG_FORMAT", "")
        
        # Auto-detect based on environment
        if not log_format:
            # Use JSON in production, console in development
            environment = os.environ.get("ENVIRONMENT", "development")
            log_format = LOG_FORMAT_JSON if environment == "production" else LOG_FORMAT_CONSOLE
    
    # Configure structlog with determined settings
    configure_structlog(log_level=log_level, log_format=log_format)


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a configured logger instance for a module.
    
    This is the main way to get loggers throughout the application.
    All loggers share the same configuration set up by setup_logging().
    
    Args:
        name: Logger name, typically __name__ from the calling module
              This helps identify the source of log entries
              Example: "cyberbullying.preprocessing", "api.routes"
    
    Returns:
        A structlog BoundLogger instance ready to use
    
    Example:
        # Get logger for this module
        logger = get_logger(__name__)
        
        # Log messages at different levels
        logger.debug("Detailed debug information")
        logger.info("Operation completed successfully", count=42)
        logger.warning("Something unexpected happened", detail="value")
        logger.error("Operation failed", error=str(exception))
        
        # Structured logging with context
        logger.info(
            "user_action",
            user_id=user_id,
            action="login",
            ip_address=ip,
        )
    """
    # Create and return a bound logger with the given name
    # The name is added to all log entries by add_logger_name processor
    return structlog.get_logger(name)


# =============================================================================
# LOG CONTEXT MANAGER
# =============================================================================

class LogContext:
    """
    Context manager for adding temporary context to logs.
    
    This class allows adding extra information to all logs within
    a specific code block. Useful for tracking requests, user actions, etc.
    
    Example:
        logger = get_logger(__name__)
        
        # Add request context to all logs in this block
        with LogContext(request_id="12345", user_id="user1"):
            logger.info("Processing request")  # Includes request_id, user_id
            logger.info("Validation passed")
            logger.warning("Slow query", duration_ms=1500)
        # Context automatically cleared after block
        
        # Context is no longer included
        logger.info("Next operation")  # No extra context
    """
    
    def __init__(self, **context: Any) -> None:
        """
        Initialize with context key-value pairs.
        
        Args:
            **context: Arbitrary key-value pairs to add to logs
                       Can be any JSON-serializable values
        
        Example:
            with LogContext(user_id="123", request_id="abc"):
                # All logs in here have user_id and request_id
                pass
        """
        # Store the context for later use
        self._context = context
        # Store previous context to restore after
        self._previous_context: Dict[str, Any] = {}
    
    def __enter__(self) -> "LogContext":
        """
        Enter the context manager.
        
        Called when entering the 'with' block.
        Binds the context to the current logger.
        
        Returns:
            Self for use inside the with block
        """
        # Bind context to structlog
        # This adds the context to all log calls until cleared
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(**self._context)
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit the context manager.
        
        Called when exiting the 'with' block.
        Clears the temporary context.
        
        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised
        
        Returns:
            None - Does not suppress exceptions
        """
        # Clear the context when exiting
        # This ensures context doesn't leak to other code
        structlog.contextvars.clear_contextvars()


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "setup_logging",      # Main logging setup function
    "get_logger",         # Get logger instance
    "LogContext",         # Context manager for temporary context
    "LOG_LEVELS",         # Log level constants
    "LOG_FORMAT_JSON",    # JSON log format constant
    "LOG_FORMAT_CONSOLE", # Console log format constant
]
