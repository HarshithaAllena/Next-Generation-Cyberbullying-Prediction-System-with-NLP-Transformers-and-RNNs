# =============================================================================
# PREPROCESSING SERVICE - MAIN API
# =============================================================================
# Purpose: FastAPI application for text preprocessing microservice.
#
# This service provides REST API endpoints for:
# - Single text preprocessing
# - Batch text preprocessing
# - Health checks
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
from contextlib import asynccontextmanager  # Async context manager
from typing import List  # Type hints

from fastapi import (
    FastAPI,  # FastAPI framework
    HTTPException,  # HTTP exceptions
    status,  # HTTP status codes
)  # FastAPI
from pydantic import BaseModel, Field  # Data validation

# Import shared components
from cyberbullying_shared_common import (
    setup_logging,  # Logging setup
    get_logger,  # Get logger
)

# Import preprocessing components
from preprocessing_service.preprocessor import (
    TextPreprocessor,  # Main preprocessor
    ProcessingResult,  # Processing result
)

# =============================================================================
# SETUP
# =============================================================================
# Initialize logging
setup_logging()

# Get logger
logger = get_logger(__name__)

# Global preprocessor instance
preprocessor: TextPreprocessor = None


# =============================================================================
# LIFESPAN
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Initializes resources on startup and cleans up on shutdown.
    """
    global preprocessor
    
    # Startup
    logger.info("Starting preprocessing service")
    
    # Initialize preprocessor
    preprocessor = TextPreprocessor(
        remove_urls=True,
        remove_emails=True,
        remove_mentions=False,
        remove_hashtags=False,
        remove_emoji=False,
        lowercase=True,
        remove_special_chars=False,
    )
    
    logger.info("Preprocessing service initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down preprocessing service")


# =============================================================================
# FASTAPI APP
# =============================================================================
# Create FastAPI application
app = FastAPI(
    title="Preprocessing Service",
    description="Text preprocessing microservice for cyberbullying detection",
    version="1.0.0",
    lifespan=lifespan,
)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class PreprocessRequest(BaseModel):
    """
    Request model for preprocessing endpoint.
    """
    text: str = Field(..., description="Text to preprocess", min_length=1)


class PreprocessResponse(BaseModel):
    """
    Response model for preprocessing endpoint.
    """
    id: str
    original_text: str
    cleaned_text: str
    is_valid: bool
    invalid_reason: str | None = None
    processing_time_ms: float


class BatchPreprocessRequest(BaseModel):
    """
    Request model for batch preprocessing.
    """
    texts: List[str] = Field(..., description="List of texts to preprocess")


class BatchPreprocessResponse(BaseModel):
    """
    Response model for batch preprocessing.
    """
    results: List[PreprocessResponse]
    total_processed: int
    processing_time_ms: float


# =============================================================================
# HEALTH ENDPOINTS
# =============================================================================

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Service health status
    """
    return {
        "status": "healthy",
        "service": "preprocessing-service",
        "version": "1.0.0",
    }


@app.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    
    Returns:
        Service readiness status
    """
    return {
        "ready": True,
        "service": "preprocessing-service",
    }


# =============================================================================
# PREPROCESSING ENDPOINTS
# =============================================================================

@app.post(
    "/preprocess",
    response_model=PreprocessResponse,
    status_code=status.HTTP_200_OK,
)
async def preprocess_text(request: PreprocessRequest):
    """
    Preprocess a single text.
    
    Args:
        request: Preprocessing request with text
    
    Returns:
        Preprocessing result
    
    Raises:
        HTTPException: If preprocessing fails
    """
    try:
        # Process text
        result = preprocessor.process(request.text)
        
        # Return response
        return PreprocessResponse(
            id=result.id,
            original_text=result.original_text,
            cleaned_text=result.cleaned_text,
            is_valid=result.is_valid,
            invalid_reason=result.invalid_reason,
            processing_time_ms=result.processing_time_ms,
        )
    
    except Exception as e:
        # Log error
        logger.error(f"Preprocessing failed: {str(e)}")
        
        # Raise HTTP exception
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Preprocessing failed: {str(e)}",
        )


@app.post(
    "/preprocess/batch",
    response_model=BatchPreprocessResponse,
    status_code=status.HTTP_200_OK,
)
async def preprocess_batch(request: BatchPreprocessRequest):
    """
    Preprocess multiple texts in batch.
    
    Args:
        request: Batch preprocessing request
    
    Returns:
        Batch preprocessing results
    
    Raises:
        HTTPException: If batch processing fails
    """
    import time
    
    start_time = time.perf_counter()
    
    try:
        # Process texts
        results = preprocessor.process_batch(request.texts)
        
        # Convert to response models
        response_results = [
            PreprocessResponse(
                id=r.id,
                original_text=r.original_text,
                cleaned_text=r.cleaned_text,
                is_valid=r.is_valid,
                invalid_reason=r.invalid_reason,
                processing_time_ms=r.processing_time_ms,
            )
            for r in results
        ]
        
        # Calculate total time
        total_time_ms = (time.perf_counter() - start_time) * 1000
        
        return BatchPreprocessResponse(
            results=response_results,
            total_processed=len(response_results),
            processing_time_ms=total_time_ms,
        )
    
    except Exception as e:
        logger.error(f"Batch preprocessing failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch preprocessing failed: {str(e)}",
        )


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
