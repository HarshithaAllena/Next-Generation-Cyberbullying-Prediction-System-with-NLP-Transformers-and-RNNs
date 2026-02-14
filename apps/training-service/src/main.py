# =============================================================================
# TRAINING SERVICE - MAIN API
# =============================================================================

from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from cyberbullying_shared_common import setup_logging, get_logger
from training_service.trainer import ModelTrainer

# Setup
setup_logging()
logger = get_logger(__name__)

# Global trainer
trainer: ModelTrainer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global trainer
    logger.info("Starting training service")
    trainer = ModelTrainer()
    logger.info("Training service initialized")
    yield
    logger.info("Shutting down training service")


# FastAPI app
app = FastAPI(
    title="Training Service",
    description="Model training microservice for cyberbullying detection",
    version="1.0.0",
    lifespan=lifespan,
)


# Models
class TrainRequest(BaseModel):
    model_architecture: str = Field(default="bert-base", description="Model architecture")
    learning_rate: float = Field(default=0.001, description="Learning rate")
    batch_size: int = Field(default=32, description="Batch size")
    epochs: int = Field(default=10, description="Number of epochs")
    train_data: List[dict] = Field(..., description="Training data")
    val_data: Optional[List[dict]] = Field(None, description="Validation data")


class EvaluateRequest(BaseModel):
    test_data: List[dict] = Field(..., description="Test data")


# Endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "training-service", "version": "1.0.0"}


@app.post("/train")
async def train_model(request: TrainRequest):
    """Train a model."""
    try:
        # Create trainer with parameters
        local_trainer = ModelTrainer(
            model_architecture=request.model_architecture,
            learning_rate=request.learning_rate,
            batch_size=request.batch_size,
            epochs=request.epochs,
        )
        
        # Train
        result = local_trainer.train(request.train_data, request.val_data)
        
        return {
            "run_id": result.run_id,
            "status": result.status,
            "metrics": result.metrics,
            "best_model_path": result.best_model_path,
            "training_time_seconds": result.training_time_seconds,
        }
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate")
async def evaluate_model(request: EvaluateRequest):
    """Evaluate a model."""
    try:
        result = trainer.evaluate(request.test_data)
        return result
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3004)
