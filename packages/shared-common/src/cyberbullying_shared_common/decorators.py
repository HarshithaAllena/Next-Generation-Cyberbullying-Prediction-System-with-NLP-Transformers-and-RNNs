# =============================================================================
# DECORATORS MODULE
# =============================================================================
# Purpose: Provides reusable decorators for common functionality across services.
#
# This module includes:
# - @retry: Automatic retry with exponential backoff
# - @cache: Function result caching (memoization)
# - @timing: Function execution time tracking
# - @validate_input: Input validation
# - @handle_exceptions: Centralized exception handling
#
# These decorators help reduce boilerplate code and ensure consistent
# behavior across all microservices.
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
# Standard library imports
import asyncio  # For async function handling
import functools  # Higher-order functions and operations on functions
import time  # Time-related functions
import logging  # Logging facility
from typing import (
    Any,  # Any type
    Callable,  # Function type
    Dict,  # Dictionary type
    Optional,  # Optional type
    Type,  # Type type
    TypeVar,  # Type variable for generics
    Union,  # Union type
)  # Type hints

# Third-party imports
from tenacity import (
    retry as tenacity_retry,  # Retry decorator from tenacity
    stop_after_attempt,  # Stop after N attempts
    wait_exponential,  # Exponential backoff
    retry_if_exception_type,  # Retry on specific exceptions
)  # Retry logic from tenacity library

# Import cache from cachetools
from cachetools import cached, TTLCache  # Caching decorators

# Import custom exceptions
from cyberbullying_shared_common.exceptions import (
    ServiceUnavailableError,
    ValidationError,
)  # Custom exception classes

# =============================================================================
# TYPE DEFINITIONS
# =============================================================================
# Type variable for function signatures
# Allows decorators to work with any function type
F = TypeVar('F', bound=Callable[..., Any])

# =============================================================================
# RETRY DECORATOR
# =============================================================================

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    logger_name: Optional[str] = None,
) -> Callable[[F], F]:
    """
    Decorator that retries a function on failure with exponential backoff.
    
    This decorator is useful for:
    - Network operations that may temporarily fail
    - External API calls that may be rate-limited
    - Database operations that may have temporary issues
    
    Args:
        max_attempts: Maximum number of attempts before giving up
                     Default: 3
        delay: Initial delay between retries in seconds
               Default: 1.0
        backoff: Multiplier for delay after each retry
                 delay * (backoff ^ attempt)
                 Default: 2.0 (1s, 2s, 4s, 8s, ...)
        exceptions: Tuple of exception types to retry on
                    Default: (Exception,) - retry on any exception
        logger_name: Optional logger name for logging retries
                     Default: None - uses function's module name
    
    Returns:
        Decorator function that wraps the original function
    
    Example:
        @retry(max_attempts=5, delay=1.0, backoff=2.0)
        def call_api(url: str) -> dict:
            response = requests.get(url)
            return response.json()
            
        # Usage
        result = call_api("https://api.example.com/data")
    """
    
    # Create decorator using tenacity
    # tenacity provides battle-tested retry logic
    return tenacity_retry(
        # Stop after max_attempts tries
        stop=stop_after_attempt(max_attempts),
        # Wait with exponential backoff
        wait=wait_exponential(
            multiplier=delay,  # Initial delay
            max=delay * (backoff ** max_attempts),  # Maximum wait
        ),
        # Retry on specified exceptions
        retry=retry_if_exception_type(exceptions),
        # Log retry attempts
        reraise=True,  # Re-raise after all attempts fail
    )


def async_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Callable[[F], F]:
    """
    Async version of retry decorator for asyncio functions.
    
    Same as retry() but designed for async/await functions.
    Uses asyncio.sleep instead of time.sleep for non-blocking delays.
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exception types to retry on
    
    Returns:
        Decorator for async functions
    
    Example:
        @async_retry(max_attempts=3)
        async def fetch_data(url: str) -> dict:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
    """
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper that handles retries for async functions.
            """
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    # Try to execute the function
                    return await func(*args, **kwargs)
                except exceptions as e:
                    # Store exception for logging
                    last_exception = e
                    
                    # Check if we have more attempts
                    if attempt < max_attempts - 1:
                        # Calculate wait time with exponential backoff
                        wait_time = delay * (backoff ** attempt)
                        # Log retry attempt
                        logging.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. "
                            f"Retrying in {wait_time:.2f}s..."
                        )
                        # Wait before next attempt (non-blocking)
                        await asyncio.sleep(wait_time)
                    else:
                        # All attempts exhausted
                        logging.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                        )
            
            # Re-raise the last exception
            raise last_exception
        
        return wrapper  # type: ignore
    
    return decorator


# =============================================================================
# CACHE DECORATOR
# =============================================================================

def cache_ttl(
    ttl: int = 300,
    maxsize: int = 128,
) -> Callable[[F], F]:
    """
    Decorator that caches function results with TTL (Time To Live).
    
    This is a memoization decorator that stores results in memory
    to avoid repeated expensive computations.
    
    Args:
        ttl: Time to live in seconds
             After this time, cached results are invalidated
             Default: 300 (5 minutes)
        maxsize: Maximum number of cached results
                 When exceeded, oldest entries are evicted
                 Default: 128
    
    Returns:
        Decorator that wraps the original function
    
    Example:
        @cache_ttl(ttl=600, maxsize=256)
        def load_model(model_path: str):
            # Expensive operation - load model from disk
            return model
        
        # First call - actually loads model
        model1 = load_model("path/to/model")
        
        # Second call - returns cached result (instant)
        model2 = load_model("path/to/model")
        
        # Same object - cache working!
        assert model1 is model2
    """
    
    # Create TTL cache
    # TTLCache automatically evicts expired entries
    cache = TTLCache(maxsize=maxsize, ttl=ttl)
    
    # Use cachetools cached decorator
    return cached(cache=cache)


def async_cache_ttl(
    ttl: int = 300,
    maxsize: int = 128,
) -> Callable[[F], F]:
    """
    Async version of cache decorator for asyncio functions.
    
    Same as cache_ttl() but designed for async/await functions.
    
    Args:
        ttl: Time to live in seconds
        maxsize: Maximum number of cached results
    
    Returns:
        Decorator for async functions
    """
    
    # Create cache
    cache = TTLCache(maxsize=maxsize, ttl=ttl)
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper that caches async function results.
            """
            # Create cache key from function name and arguments
            # Simple approach: use function name + str(args) + str(kwargs)
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Check if result is cached
            if key in cache:
                return cache[key]
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache[key] = result
            
            return result
        
        return wrapper  # type: ignore
    
    return decorator


# =============================================================================
# TIMING DECORATOR
# =============================================================================

def timing(func: Optional[Callable] = None, *, logger_name: Optional[str] = None) -> Any:
    """
    Decorator that measures and logs function execution time.
    
    This decorator is useful for:
    - Performance monitoring
    - Identifying slow operations
    - Profiling function execution
    
    Args:
        func: The function to wrap (if used without parentheses)
        logger_name: Optional logger name for logging timing
                    Default: None - uses function's module name
    
    Returns:
        Decorated function that logs execution time
    
    Example:
        @timing
        def process_data(data: list) -> list:
            return [x * 2 for x in data]
            
        # Output: "Function 'process_data' took 0.00123 seconds"
    """
    
    # Handle both @timing and @timing() syntax
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper that measures and logs execution time.
            """
            # Get logger
            log = logging.getLogger(logger_name or f.__module__)
            
            # Record start time
            start_time = time.perf_counter()
            
            try:
                # Execute the function
                result = f(*args, **kwargs)
                return result
            finally:
                # Calculate elapsed time
                elapsed_time = time.perf_counter() - start_time
                
                # Log the timing
                # Using INFO level for important timings
                # Using DEBUG for very fast operations (< 1ms)
                if elapsed_time > 1.0:
                    log.warning(
                        f"Function '{f.__name__}' took {elapsed_time:.2f} seconds"
                    )
                elif elapsed_time > 0.001:
                    log.info(
                        f"Function '{f.__name__}' took {elapsed_time:.4f} seconds"
                    )
                else:
                    log.debug(
                        f"Function '{f.__name__}' took {elapsed_time:.6f} seconds"
                    )
        
        return wrapper
    
    # Handle @timing vs @timing()
    if func is None:
        # Called as @timing() or @timing(logger_name="x")
        return decorator
    else:
        # Called as @timing
        return decorator(func)


def async_timing(func: Optional[Callable] = None, *, logger_name: Optional[str] = None) -> Any:
    """
    Async version of timing decorator for asyncio functions.
    
    Same as timing() but designed for async/await functions.
    
    Args:
        func: The async function to wrap
        logger_name: Optional logger name
    
    Returns:
        Decorated async function that logs execution time
    """
    
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper that measures and logs async execution time.
            """
            # Get logger
            log = logging.getLogger(logger_name or f.__module__)
            
            # Record start time
            start_time = time.perf_counter()
            
            try:
                # Execute the async function
                result = await f(*args, **kwargs)
                return result
            finally:
                # Calculate elapsed time
                elapsed_time = time.perf_counter() - start_time
                
                # Log the timing
                log.info(
                    f"Async function '{f.__name__}' took {elapsed_time:.4f} seconds"
                )
        
        return wrapper
    
    # Handle @async_timing vs @async_timing()
    if func is None:
        return decorator
    else:
        return decorator(func)


# =============================================================================
# VALIDATION DECORATOR
# =============================================================================

def validate_input(**validators: Dict[str, Callable[[Any], bool]]) -> Callable[[F], F]:
    """
    Decorator that validates function input arguments.
    
    This decorator checks input arguments against validation functions
    before executing the function body.
    
    Args:
        **validators: Keyword arguments mapping parameter names to validator functions
                      Each validator should return True if valid, False otherwise
    
    Returns:
        Decorator that validates inputs before function execution
    
    Example:
        @validate_input(
            # Validate 'text' parameter is non-empty string
            text=lambda x: isinstance(x, str) and len(x) > 0,
            # Validate 'max_length' is positive integer
            max_length=lambda x: isinstance(x, int) and x > 0,
        )
        def process_text(text: str, max_length: int = 100) -> str:
            return text[:max_length]
            
        # Valid call
        process_text("Hello", max_length=10)
        
        # Raises ValidationError for invalid input
        process_text("")  # ValidationError: text failed validation
    """
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper that validates inputs before execution.
            """
            # Get function signature to map args to parameter names
            import inspect
            sig = inspect.signature(func)
            
            # Create bound arguments object
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate each parameter
            for param_name, validator in validators.items():
                # Get the argument value
                value = bound_args.arguments.get(param_name)
                
                # Run validator
                if value is not None and not validator(value):
                    # Raise validation error with descriptive message
                    raise ValidationError(
                        f"Parameter '{param_name}' failed validation for function '{func.__name__}'. "
                        f"Value: {value!r}"
                    )
            
            # All validations passed - execute function
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore
    
    return decorator


# =============================================================================
# EXCEPTION HANDLING DECORATOR
# =============================================================================

def handle_exceptions(
    exceptions: tuple = (Exception,),
    default_return: Any = None,
    log_errors: bool = True,
    reraise: bool = False,
) -> Callable[[F], F]:
    """
    Decorator that handles exceptions with configurable behavior.
    
    This decorator provides centralized exception handling with:
    - Configurable exception types to catch
    - Default return value on failure
    - Optional error logging
    - Optional re-raising
    
    Args:
        exceptions: Tuple of exception types to catch
                    Default: (Exception,) - catch all exceptions
        default_return: Value to return when exception occurs
                       Default: None
        log_errors: Whether to log the exception
                   Default: True
        reraise: Whether to re-raise the exception after handling
                 Default: False
    
    Returns:
        Decorator that handles exceptions
    
    Example:
        @handle_exceptions(
            exceptions=(ValueError, KeyError),
            default_return={"error": "Invalid input"},
            log_errors=True,
            reraise=False,
        )
        def parse_input(data: dict) -> dict:
            return data["key"]
    """
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper that handles exceptions.
            """
            try:
                # Try to execute the function
                return func(*args, **kwargs)
            except exceptions as e:
                # Get logger for this function
                log = logging.getLogger(func.__module__)
                
                # Log the error if enabled
                if log_errors:
                    log.error(
                        f"Exception in '{func.__name__}': {type(e).__name__}: {e}",
                        exc_info=True,  # Include stack trace
                    )
                
                # Re-raise if enabled
                if reraise:
                    raise
                
                # Return default value
                return default_return
        
        return wrapper  # type: ignore
    
    return decorator


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "retry",              # Retry with exponential backoff
    "async_retry",       # Async retry decorator
    "cache_ttl",         # Cache with time-to-live
    "cache",             # Alias for cache_ttl
    "async_cache_ttl",   # Async cache decorator
    "timing",            # Function timing
    "async_timing",      # Async function timing
    "validate_input",     # Input validation
    "handle_exceptions",  # Exception handling
]

# Alias for cache_ttl
cache = cache_ttl
