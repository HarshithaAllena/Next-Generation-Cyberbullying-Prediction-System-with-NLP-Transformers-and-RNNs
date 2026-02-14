# =============================================================================
# PREDICTION SERVICE - MAIN API
# =============================================================================

from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from cyberbullying_shared_common import setup_logging, get_logger
from prediction_service.predictor import ModelPredictor

# Setup
setup_logging()
logger = get_logger(__name__)

# Global predictor
predictor: ModelPredictor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global predictor
    logger.info("Starting prediction service")
    predictor = ModelPredictor()
    logger.info("Prediction service initialized")
    yield
    logger.info("Shutting down prediction service")


# FastAPI app
app = FastAPI(
    title="Prediction Service",
    description="Prediction microservice for cyberbullying detection",
    version="1.0.0",
    lifespan=lifespan,
)


# Models
class PredictRequest(BaseModel):
    text: str = Field(..., description="Text to predict")
    text_id: Optional[str] = Field(None, description="Optional text ID")


class PredictResponse(BaseModel):
    text_id: str
    predicted_label: str
    confidence: float
    probabilities: dict
    is_high_confidence: bool
    model_version: str
    inference_time_ms: float


class BatchPredictRequest(BaseModel):
    texts: List[str] = Field(..., description="Texts to predict")


# Endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "prediction-service", "version": "1.0.0"}


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """Predict cyberbullying for single text."""
    try:
        result = predictor.predict(request.text, request.text_id)
        return PredictResponse(
            text_id=result.text_id,
            predicted_label=result.predicted_label,
            confidence=result.confidence,
            probabilities=result.probabilities,
            is_high_confidence=result.is_high_confidence,
            model_version=result.model_version,
            inference_time_ms=result.inference_time_ms,
        )
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch")
async def predict_batch(request: BatchPredictRequest):
    """Predict cyberbullying for multiple texts."""
    try:
        results = predictor.predict_batch(request.texts)
        return {
            "predictions": [
                {
                    "text_id": r.text_id,
                    "predicted_label": r.predicted_label,
                    "confidence": r.confidence,
                    "probabilities": r.probabilities,
                    "is_high_confidence": r.is_high_confidence,
                    "inference_time_ms": r.inference_time_ms,
                }
                for r in results
            ],
            "total_processed": len(results),
        }
    except Exception as e:
        logger.error(f"Batch prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3003)
