# =============================================================================
# EXCEPTIONS MODULE
# =============================================================================
# Purpose: Defines custom exception classes for the Cyberbullying NLP system.
#
# This module provides:
# - Base exception class for all custom exceptions
# - Domain-specific exceptions (validation, preprocessing, model, etc.)
# - HTTP-compatible exceptions for API error handling
#
# Using custom exceptions allows:
# - Better error handling and debugging
# - Structured error responses in APIs
# - Easier error categorization and logging
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
# Standard library for exception base classes
from typing import Any, Dict, Optional  # Type hints

# =============================================================================
# BASE EXCEPTION CLASS
# =============================================================================

class CyberbullyingError(Exception):
    """
    Base exception class for all Cyberbullying NLP errors.
    
    This is the parent class for all custom exceptions in the system.
    It provides common functionality like error codes and additional context.
    
    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code for programmatic handling
        details: Additional context about the error
        service: Name of the service where error occurred
    
    Example:
        try:
            # Some operation
            raise CyberbullyingError(
                message="Model loading failed",
                error_code="MODEL_LOAD_ERROR",
                details={"model_path": "/path/to/model"},
                service="prediction-service"
            )
        except CyberbullyingError as e:
            print(f"Error: {e.message}, Code: {e.error_code}")
    """
    
    # Default error code if not specified
    DEFAULT_ERROR_CODE = "INTERNAL_ERROR"
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None,
    ) -> None:
        """
        Initialize the exception.
        
        Args:
            message: Human-readable error message describing what went wrong
            error_code: Machine-readable code for programmatic handling
                       Defaults to "INTERNAL_ERROR"
            details: Additional context data for debugging
                    Can include parameters, file paths, etc.
            service: Name of the service where error occurred
                   Helps with distributed error tracking
        """
        # Call parent exception __init__
        super().__init__(message)
        
        # Store error information as instance attributes
        self.message = message  # Error message
        self.error_code = error_code or self.DEFAULT_ERROR_CODE  # Error code
        self.details = details or {}  # Additional details
        self.service = service  # Service name
    
    def __str__(self) -> str:
        """
        String representation of the exception.
        
        Returns:
            Formatted string with error code and message
        """
        # Format: [ERROR_CODE] message
        return f"[{self.error_code}] {self.message}"
    
    def __repr__(self) -> str:
        """
        Developer representation of the exception.
        
        Returns:
            String with all error details
        """
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"error_code={self.error_code!r}, "
            f"details={self.details!r}, "
            f"service={self.service!r})"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary for JSON serialization.
        
        This is useful for API error responses.
        
        Returns:
            Dictionary with error information
        """
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "service": self.service,
            "exception_type": self.__class__.__name__,
        }


# =============================================================================
# VALIDATION EXCEPTIONS
# =============================================================================

class ValidationError(CyberbullyingError):
    """
    Exception raised for data validation failures.
    
    This exception is raised when:
    - Input data doesn't meet schema requirements
    - Required fields are missing
    - Data format is incorrect
    - Business validation rules are violated
    
    Example:
        raise ValidationError(
            message="Text cannot be empty",
            error_code="VALIDATION_ERROR",
            details={"field": "text", "value": ""}
        )
    """
    
    # Error code for validation errors
    DEFAULT_ERROR_CODE = "VALIDATION_ERROR"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize validation error.
        
        Args:
            message: Description of validation failure
            details: Additional validation context
        """
        super().__init__(
            message=message,
            error_code=self.DEFAULT_ERROR_CODE,
            details=details,
        )


# =============================================================================
# PREPROCESSING EXCEPTIONS
# =============================================================================

class PreprocessingError(CyberbullyingError):
    """
    Exception raised during text preprocessing.
    
    This exception is raised when:
    - Text cleaning fails
    - Tokenization encounters unsupported format
    - Language detection fails
    - Text normalization encounters errors
    
    Example:
        raise PreprocessingError(
            message="Failed to tokenize text",
            details={"text_length": 50000, "max_supported": 10000}
        )
    """
    
    # Error code for preprocessing errors
    DEFAULT_ERROR_CODE = "PREPROCESSING_ERROR"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize preprocessing error.
        
        Args:
            message: Description of preprocessing failure
            details: Additional preprocessing context
        """
        super().__init__(
            message=message,
            error_code=self.DEFAULT_ERROR_CODE,
            details=details,
        )


# =============================================================================
# MODEL EXCEPTIONS
# =============================================================================

class ModelError(CyberbullyingError):
    """
    Exception raised for model-related errors.
    
    This exception is raised when:
    - Model loading fails
    - Model file is corrupted
    - Model architecture doesn't match
    - Inference encounters errors
    
    Example:
        raise ModelError(
            message="Failed to load model weights",
            details={"model_path": "/models/bert-base", "error": "FileNotFound"}
        )
    """
    
    # Error code for model errors
    DEFAULT_ERROR_CODE = "MODEL_ERROR"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize model error.
        
        Args:
            message: Description of model failure
            details: Additional model context
        """
        super().__init__(
            message=message,
            error_code=self.DEFAULT_ERROR_CODE,
            details=details,
        )


class ModelNotFoundError(ModelError):
    """
    Exception raised when a model is not found.
    
    This exception is raised when:
    - Requested model version doesn't exist
    - Model registry doesn't have the model
    - Model files are missing
    
    Example:
        raise ModelNotFoundError(
            message="Model version 'v1.2.3' not found",
            details={"model_name": "cyberbullying-detector", "version": "v1.2.3"}
        )
    """
    
    DEFAULT_ERROR_CODE = "MODEL_NOT_FOUND"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize model not found error.
        
        Args:
            message: Description of missing model
            details: Additional context
        """
        super().__init__(message=message, details=details)


class ModelLoadingError(ModelError):
    """
    Exception raised when model loading fails.
    
    This exception is raised when:
    - Model file cannot be read
    - Model configuration is invalid
    - Dependencies are missing
    
    Example:
        raise ModelLoadingError(
            message="Failed to load PyTorch model",
            details={"model_path": "/models/bert.pt", "error": "RuntimeError"}
        )
    """
    
    DEFAULT_ERROR_CODE = "MODEL_LOAD_ERROR"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize model loading error.
        
        Args:
            message: Description of loading failure
            details: Additional context
        """
        super().__init__(message=message, details=details)


# =============================================================================
# TRAINING EXCEPTIONS
# =============================================================================

class TrainingError(CyberbullyingError):
    """
    Exception raised during model training.
    
    This exception is raised when:
    - Training data cannot be loaded
    - Training loop encounters errors
    - Gradient computation fails
    - Checkpoint saving fails
    
    Example:
        raise TrainingError(
            message="Training data not found",
            details={"data_path": "/data/train.csv"}
        )
    """
    
    # Error code for training errors
    DEFAULT_ERROR_CODE = "TRAINING_ERROR"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize training error.
        
        Args:
            message: Description of training failure
            details: Additional training context
        """
        super().__init__(
            message=message,
            error_code=self.DEFAULT_ERROR_CODE,
            details=details,
        )


class TrainingDataError(TrainingError):
    """
    Exception raised for training data issues.
    
    This exception is raised when:
    - Dataset cannot be loaded
    - Dataset format is incorrect
    - Dataset is empty or too small
    
    Example:
        raise TrainingDataError(
            message="Dataset is empty",
            details={"data_path": "/data/train.csv", "rows": 0}
        )
    """
    
    DEFAULT_ERROR_CODE = "TRAINING_DATA_ERROR"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize training data error.
        
        Args:
            message: Description of data issue
            details: Additional data context
        """
        super().__init__(message=message, details=details)


# =============================================================================
# PREDICTION EXCEPTIONS
# =============================================================================

class PredictionError(CyberbullyingError):
    """
    Exception raised during prediction/inference.
    
    This exception is raised when:
    - Model prediction fails
    - Input preprocessing fails
    - Output postprocessing fails
    - Prediction timeout occurs
    
    Example:
        raise PredictionError(
            message="Prediction timeout",
            details={"timeout_ms": 5000, "text_length": 5000}
        )
    """
    
    # Error code for prediction errors
    DEFAULT_ERROR_CODE = "PREDICTION_ERROR"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize prediction error.
        
        Args:
            message: Description of prediction failure
            details: Additional prediction context
        """
        super().__init__(
            message=message,
            error_code=self.DEFAULT_ERROR_CODE,
            details=details,
        )


class PredictionTimeoutError(PredictionError):
    """
    Exception raised when prediction exceeds time limit.
    
    Example:
        raise PredictionTimeoutError(
            message="Prediction exceeded 5 second limit",
            details={"text_length": 10000, "elapsed_ms": 5200}
        )
    """
    
    DEFAULT_ERROR_CODE = "PREDICTION_TIMEOUT"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize prediction timeout error.
        
        Args:
            message: Description of timeout
            details: Additional timeout context
        """
        super().__init__(message=message, details=details)


# =============================================================================
# SERVICE EXCEPTIONS
# =============================================================================

class ServiceUnavailableError(CyberbullyingError):
    """
    Exception raised when a service is unavailable.
    
    This exception is raised when:
    - External service is down
    - Service cannot be reached
    - Service timeout occurs
    
    Example:
        raise ServiceUnavailableError(
            message="Feature service unavailable",
            details={"service": "feature-service", "endpoint": "http://feature:3002"}
        )
    """
    
    # Error code for service unavailability
    DEFAULT_ERROR_CODE = "SERVICE_UNAVAILABLE"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize service unavailable error.
        
        Args:
            message: Description of service failure
            details: Additional service context
        """
        super().__init__(
            message=message,
            error_code=self.DEFAULT_ERROR_CODE,
            details=details,
        )


class ServiceConnectionError(ServiceUnavailableError):
    """
    Exception raised when connection to service fails.
    
    Example:
        raise ServiceConnectionError(
            message="Cannot connect to preprocessing service",
            details={"service": "preprocessing-service", "error": "ConnectionRefused"}
        )
    """
    
    DEFAULT_ERROR_CODE = "SERVICE_CONNECTION_ERROR"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize service connection error.
        
        Args:
            message: Description of connection failure
            details: Additional connection context
        """
        super().__init__(message=message, details=details)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Base exception
    "CyberbullyingError",
    # Validation
    "ValidationError",
    # Preprocessing
    "PreprocessingError",
    # Model
    "ModelError",
    "ModelNotFoundError",
    "ModelLoadingError",
    # Training
    "TrainingError",
    "TrainingDataError",
    # Prediction
    "PredictionError",
    "PredictionTimeoutError",
    # Service
    "ServiceUnavailableError",
    "ServiceConnectionError",
]
