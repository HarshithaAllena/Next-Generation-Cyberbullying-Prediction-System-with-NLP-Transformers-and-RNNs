# =============================================================================
# CONFIGURATION MODULE
# =============================================================================
# Purpose: Centralized configuration management using Pydantic Settings.
#
# This module provides:
# - Environment-based configuration
# - Type-safe settings with validation
# - Default values for all services
# - Configuration for all microservices
#
# Usage:
#     from cyberbullying_shared_common import get_settings
#     
#     settings = get_settings()
#     print(settings.database.url)
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
# Pydantic imports for settings management
from pydantic import Field  # Field configuration
from pydantic_settings import (
    BaseSettings,  # Base settings class
    SettingsConfigDict,  # Settings configuration
)

# Type hints
from typing import Dict, List, Optional  # Type hints

# =============================================================================
# BASE SETTINGS CLASS
# =============================================================================

class Settings(BaseSettings):
    """
    Base settings class for all services.
    
    This class provides common configuration that applies
    to all microservices in the system.
    
    Settings are loaded from:
    1. Environment variables (highest priority)
    2. .env file (if present)
    3. Default values (lowest priority)
    
    Example:
        # Environment variables
        export ENVIRONMENT=production
        export LOG_LEVEL=DEBUG
        
        # In code
        settings = get_settings()
        print(settings.environment)  # "production"
    """
    
    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        # Load from .env file
        env_file=".env",
        # Environment variables prefix
        env_prefix="",
        # Case-sensitive environment variables
        case_sensitive=False,
        # Extra fields are forbidden (strict mode)
        extra="ignore",
    )
    
    # =====================================================================
    # ENVIRONMENT SETTINGS
    # =====================================================================
    
    # Application environment
    environment: str = Field(
        default="development",
        description="Application environment: development, staging, production",
    )
    
    # Debug mode
    debug: bool = Field(
        default=False,
        description="Enable debug mode for additional logging",
    )
    
    # =====================================================================
    # LOGGING SETTINGS
    # =====================================================================
    
    # Log level
    log_level: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
    )
    
    # Log format
    log_format: str = Field(
        default="json",
        description="Log format: json or console",
    )
    
    # =====================================================================
    # API SETTINGS
    # =====================================================================
    
    # API title
    api_title: str = Field(
        default="Cyberbullying NLP API",
        description="API title for documentation",
    )
    
    # API version
    api_version: str = Field(
        default="1.0.0",
        description="API version",
    )
    
    # API prefix
    api_prefix: str = Field(
        default="/api/v1",
        description="API route prefix",
    )
    
    # =====================================================================
    # CORS SETTINGS
    # =====================================================================
    
    # Allowed CORS origins
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )
    
    # Allow credentials
    cors_allow_credentials: bool = Field(
        default=True,
        description="Allow credentials in CORS",
    )
    
    # =====================================================================
    # RATE LIMITING
    # =====================================================================
    
    # Rate limit max requests
    rate_limit_max: int = Field(
        default=100,
        description="Maximum requests per time window",
    )
    
    # Rate limit window in seconds
    rate_limit_window: int = Field(
        default=60,
        description="Rate limit time window in seconds",
    )
    
    # =====================================================================
    # DATABASE SETTINGS
    # =====================================================================
    
    # Database URL
    database_url: str = Field(
        default="postgresql://cyberbullying:password@localhost:5432/cyberbullying",
        description="PostgreSQL database URL",
    )
    
    # Database pool size
    database_pool_size: int = Field(
        default=10,
        description="Database connection pool size",
    )
    
    # Database max overflow
    database_max_overflow: int = Field(
        default=20,
        description="Database max overflow connections",
    )
    
    # =====================================================================
    # REDIS SETTINGS
    # =====================================================================
    
    # Redis URL
    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis URL for caching",
    )
    
    # Redis cache TTL
    redis_cache_ttl: int = Field(
        default=300,
        description="Default cache TTL in seconds",
    )
    
    # =====================================================================
    # SERVICE URLs
    # =====================================================================
    
    # Preprocessing service URL
    preprocessing_service_url: str = Field(
        default="http://localhost:3001",
        description="Preprocessing service URL",
    )
    
    # Feature service URL
    feature_service_url: str = Field(
        default="http://localhost:3002",
        description="Feature service URL",
    )
    
    # Prediction service URL
    prediction_service_url: str = Field(
        default="http://localhost:3003",
        description="Prediction service URL",
    )
    
    # Training service URL
    training_service_url: str = Field(
        default="http://localhost:3004",
        description="Training service URL",
    )
    
    # Explainability service URL
    explainability_service_url: str = Field(
        default="http://localhost:3005",
        description="Explainability service URL",
    )
    
    # Model registry URL
    model_registry_url: str = Field(
        default="http://localhost:3006",
        description="Model registry URL",
    )
    
    # Monitoring service URL
    monitoring_service_url: str = Field(
        default="http://localhost:3007",
        description="Monitoring service URL",
    )
    
    # =====================================================================
    # MLFLOW SETTINGS
    # =====================================================================
    
    # MLflow tracking URI
    mlflow_tracking_uri: str = Field(
        default="http://localhost:5000",
        description="MLflow tracking server URI",
    )
    
    # MLflow experiment name
    mlflow_experiment: str = Field(
        default="cyberbullying-nlp",
        description="Default MLflow experiment name",
    )
    
    # =====================================================================
    # MODEL SETTINGS
    # =====================================================================
    
    # Default model name
    default_model_name: str = Field(
        default="cyberbullying-detector",
        description="Default model name",
    )
    
    # Default model version
    default_model_version: str = Field(
        default="latest",
        description="Default model version",
    )
    
    # Model cache directory
    model_cache_dir: str = Field(
        default="/app/models",
        description="Directory for cached models",
    )
    
    # =====================================================================
    # PREPROCESSING SETTINGS
    # =====================================================================
    
    # Maximum text length
    max_text_length: int = Field(
        default=10000,
        description="Maximum text length to process",
    )
    
    # Minimum text length
    min_text_length: int = Field(
        default=3,
        description="Minimum text length after preprocessing",
    )
    
    # Supported languages
    supported_languages: List[str] = Field(
        default=["en", "es", "fr", "de"],
        description="Supported languages for processing",
    )
    
    # =====================================================================
    # EMBEDDING SETTINGS
    # =====================================================================
    
    # Embedding model name
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Default embedding model",
    )
    
    # Maximum sequence length
    max_seq_length: int = Field(
        default=512,
        description="Maximum sequence length for embeddings",
    )
    
    # Embedding batch size
    embedding_batch_size: int = Field(
        default=32,
        description="Batch size for embedding generation",
    )
    
    # =====================================================================
    # TRAINING SETTINGS
    # =====================================================================
    
    # Default epochs
    default_epochs: int = Field(
        default=10,
        description="Default number of training epochs",
    )
    
    # Default batch size
    default_batch_size: int = Field(
        default=32,
        description="Default training batch size",
    )
    
    # Default learning rate
    default_learning_rate: float = Field(
        default=0.001,
        description="Default learning rate",
    )
    
    # Checkpoint directory
    checkpoint_dir: str = Field(
        default="/app/checkpoints",
        description="Directory for model checkpoints",
    )
    
    # =====================================================================
    # PREDICTION SETTINGS
    # =====================================================================
    
    # Prediction timeout in milliseconds
    prediction_timeout_ms: int = Field(
        default=5000,
        description="Prediction timeout in milliseconds",
    )
    
    # Confidence threshold
    confidence_threshold: float = Field(
        default=0.5,
        description="Minimum confidence threshold for predictions",
    )
    
    # Max batch size for predictions
    prediction_max_batch_size: int = Field(
        default=64,
        description="Maximum batch size for predictions",
    )
    
    # =====================================================================
    # SECURITY SETTINGS
    # =====================================================================
    
    # JWT secret key
    jwt_secret: str = Field(
        default="development-secret-key-change-in-production",
        description="JWT secret key for token signing",
    )
    
    # JWT algorithm
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT algorithm for token signing",
    )
    
    # JWT expiration in minutes
    jwt_expiration_minutes: int = Field(
        default=60,
        description="JWT token expiration in minutes",
    )
    
    # =====================================================================
    # FEATURE FLAGS
    # =====================================================================
    
    # Enable GPU
    enable_gpu: bool = Field(
        default=False,
        description="Enable GPU acceleration",
    )
    
    # Enable caching
    enable_cache: bool = Field(
        default=True,
        description="Enable result caching",
    )
    
    # Enable monitoring
    enable_monitoring: bool = Field(
        default=True,
        description="Enable monitoring and metrics",
    )
    
    # =====================================================================
    # CLASS METHODS
    # =====================================================================
    
    def is_production(self) -> bool:
        """
        Check if running in production environment.
        
        Returns:
            True if environment is 'production'
        """
        return self.environment == "production"
    
    def is_development(self) -> bool:
        """
        Check if running in development environment.
        
        Returns:
            True if environment is 'development'
        """
        return self.environment == "development"
    
    def is_staging(self) -> bool:
        """
        Check if running in staging environment.
        
        Returns:
            True if environment is 'staging'
        """
        return self.environment == "staging"


# =============================================================================
# SETTINGS INSTANCES
# =============================================================================

# Global settings instance - singleton pattern
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    This function returns a singleton instance of Settings
    that is shared across the application.
    
    Returns:
        Settings instance with configuration
    
    Example:
        settings = get_settings()
        print(settings.database_url)
    """
    global _settings_instance
    
    # Create instance if not exists
    if _settings_instance is None:
        _settings_instance = Settings()
    
    return _settings_instance


def reset_settings() -> None:
    """
    Reset the settings instance.
    
    This is useful for testing to ensure a fresh
    settings instance is created.
    """
    global _settings_instance
    _settings_instance = None


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "Settings",           # Base settings class
    "get_settings",      # Get settings singleton
    "reset_settings",    # Reset settings instance
]
