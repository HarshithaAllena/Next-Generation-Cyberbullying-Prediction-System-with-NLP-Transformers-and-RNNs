# =============================================================================
# SHARED COMMON PACKAGE - __init__.py
# =============================================================================
# Purpose: Shared utilities, decorators, and helpers used across all services
# in the Cyberbullying NLP Monorepo.
#
# This package provides:
# - Logging configuration
# - Decorators (timing, retry, caching)
# - Common utilities (file handling, formatting)
# - Exception classes
# - Configuration management
#
# Key Modules:
# - logging_config: Centralized logging setup
# - decorators: Reusable decorators (retry, cache, timing)
# - exceptions: Custom exception classes
# - utils: Common utility functions
# - config: Configuration management
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

"""
Cyberbullying NLP - Shared Common Package

This package provides shared utilities and common functionality used across
all microservices in the monorepo. It ensures consistency and reduces
code duplication.

Example Usage:
    from cyberbullying_shared_common import setup_logging, retry, cache
    
    # Setup logging
    setup_logging()
    
    # Use decorator
    @retry(max_attempts=3, delay=1)
    def my_function():
        pass
"""

# =============================================================================
# VERSION
# =============================================================================
# Current version of the shared common package
__version__ = "1.0.0"

# =============================================================================
# IMPORTS - Core Modules
# =============================================================================
# Import main components for easy access
# These imports provide the public API of this package

# Logging configuration and utilities
from cyberbullying_shared_common.logging_config import (
    setup_logging,
    get_logger,
    LogContext,
)

# Decorators for common functionality
from cyberbullying_shared_common.decorators import (
    retry,
    cache_ttl as cache,
    timing,
    async_timing,
    validate_input,
    handle_exceptions,
)

# Custom exception classes
from cyberbullying_shared_common.exceptions import (
    CyberbullyingError,
    ValidationError,
    ModelError,
    PreprocessingError,
    PredictionError,
    TrainingError,
    ServiceUnavailableError,
)

# Utility functions
from cyberbullying_shared_common.utils import (
    generate_uuid,
    load_json,
    save_json,
    ensure_dir,
    get_timestamp,
)

# Configuration management
from cyberbullying_shared_common.config import (
    Settings,
    get_settings,
)

# =============================================================================
# PUBLIC API
# =============================================================================
# Define what's exported when using: from cyberbullying_shared_common import *

__all__ = [
    # Version
    "__version__",
    # Logging
    "setup_logging",
    "get_logger",
    "LogContext",
    # Decorators
    "retry",
    "cache",
    "timing",
    "async_timing",
    "validate_input",
    "handle_exceptions",
    # Exceptions
    "CyberbullyingError",
    "ValidationError",
    "ModelError",
    "PreprocessingError",
    "PredictionError",
    "TrainingError",
    "ServiceUnavailableError",
    # Utils
    "generate_uuid",
    "load_json",
    "save_json",
    "ensure_dir",
    "get_timestamp",
    # Config
    "Settings",
    "get_settings",
]

# =============================================================================
# PACKAGE INITIALIZATION
# =============================================================================
# This code runs when the package is imported
# Can be used for one-time initialization

def _initialize_package():
    """
    Package initialization code.
    Runs once when the package is first imported.
    """
    # Log package initialization (deferred to avoid circular imports)
    pass

# Run initialization
_initialize_package()
