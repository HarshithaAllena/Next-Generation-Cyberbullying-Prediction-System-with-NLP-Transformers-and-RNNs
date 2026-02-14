# =============================================================================
# FEATURE SERVICE - MAIN API
# =============================================================================

from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from cyberbullying_shared_common import setup_logging, get_logger
from feature_service.extractor import FeatureExtractor, FeatureResult

# Setup
setup_logging()
logger = get_logger(__name__)

# Global instances
extractor: FeatureExtractor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global extractor
    logger.info("Starting feature service")
    extractor = FeatureExtractor()
    logger.info("Feature service initialized")
    yield
    logger.info("Shutting down feature service")


# FastAPI app
app = FastAPI(
    title="Feature Service",
    description="Feature extraction microservice for cyberbullying detection",
    version="1.0.0",
    lifespan=lifespan,
)


# Models
class ExtractFeaturesRequest(BaseModel):
    text: str = Field(..., description="Preprocessed text")
    text_id: str = Field(None, description="Optional text ID")


class ExtractFeaturesResponse(BaseModel):
    id: str
    text_id: str
    preprocessed_text: str
    statistical_features: dict
    social_features: dict
    linguistic_features: dict
    extraction_time_ms: float


# Endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "feature-service", "version": "1.0.0"}


@app.post("/extract", response_model=ExtractFeaturesResponse)
async def extract_features(request: ExtractFeaturesRequest):
    """Extract features from text."""
    try:
        result = extractor.extract(request.text, request.text_id)
        return ExtractFeaturesResponse(
            id=result.id,
            text_id=result.text_id,
            preprocessed_text=result.preprocessed_text,
            statistical_features=result.statistical_features,
            social_features=result.social_features,
            linguistic_features=result.linguistic_features,
            extraction_time_ms=result.extraction_time_ms,
        )
    except Exception as e:
        logger.error(f"Feature extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract/batch")
async def extract_features_batch(texts: List[str]):
    """Extract features from multiple texts."""
    try:
        results = extractor.extract_batch(texts)
        return {
            "results": [
                {
                    "id": r.id,
                    "text_id": r.text_id,
                    "statistical_features": r.statistical_features,
                    "social_features": r.social_features,
                    "linguistic_features": r.linguistic_features,
                    "extraction_time_ms": r.extraction_time_ms,
                }
                for r in results
            ],
            "total_processed": len(results),
        }
    except Exception as e:
        logger.error(f"Batch feature extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3002)
