# =============================================================================
# API GATEWAY - MAIN APPLICATION
# =============================================================================
# Purpose: Main API gateway that routes requests to microservices.

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from cyberbullying_shared_common import setup_logging, get_logger

# Setup
setup_logging()
logger = get_logger(__name__)


# =============================================================================
# LIFESPAN
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan."""
    logger.info("Starting API Gateway")
    logger.info("API Gateway initialized")
    yield
    logger.info("Shutting down API Gateway")


# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(
    title="Cyberbullying Detection API",
    description="Main API Gateway for Next-Generation Cyberbullying Prediction System",
    version="1.0.0",
    lifespan=lifespan,
)


# =============================================================================
# CORS
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# MODELS
# =============================================================================

class ClassifyRequest(BaseModel):
    """Request for text classification."""
    text: str = Field(..., description="Text to classify", min_length=1)
    include_explanation: bool = Field(False, description="Include explanation")


class ClassifyResponse(BaseModel):
    """Response for text classification."""
    text_id: str
    predicted_label: str
    confidence: float
    probabilities: dict
    is_high_confidence: bool
    model_version: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "message": "Cyberbullying Detection API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="api-gateway",
        version="1.0.0",
    )


@app.post("/classify", response_model=ClassifyResponse)
async def classify_text(request: ClassifyRequest):
    """
    Classify text for cyberbullying detection.
    
    This is the main endpoint that:
    1. Receives text
    2. Sends to preprocessing service
    3. Sends to feature service
    4. Sends to prediction service
    5. Returns result
    """
    import uuid
    
    text_id = str(uuid.uuid4())
    
    # For now, simulate the full pipeline
    # In production, this would call actual services
    
    # Simulated prediction result
    import random
    random.seed(hash(request.text) % 10000)
    
    labels = ["bullying", "not_bullying", "harassment", "hate_speech"]
    probs = [random.random() for _ in labels]
    total = sum(probs)
    probabilities = {label: prob / total for label, prob in zip(labels, probs)}
    
    predicted = max(probabilities, key=probabilities.get)
    confidence = probabilities[predicted]
    
    return ClassifyResponse(
        text_id=text_id,
        predicted_label=predicted,
        confidence=confidence,
        probabilities=probabilities,
        is_high_confidence=confidence >= 0.5,
        model_version="1.0.0",
    )


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
