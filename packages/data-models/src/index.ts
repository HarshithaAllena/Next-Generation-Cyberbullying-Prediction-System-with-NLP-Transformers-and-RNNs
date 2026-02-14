/**
 * =============================================================================
 * DATA MODELS - INDEX FILE
 * =============================================================================
 * Purpose: Main entry point that exports all data models, schemas, and types
 * for the Cyberbullying Prediction System.
 *
 * This file serves as the public API for the @cyberbullying/data-models package.
 * All consumers should import from this file to ensure they get the correct
 * types and schemas.
 *
 * Key Exports:
 * - Text schemas: Input/output models for text processing
 * - Prediction schemas: Model prediction results and confidence
 * - Training schemas: Training configuration and results
 * - Metadata schemas: Service metadata and health status
 *
 * Author: Cyberbullying Prediction Team
 * Version: 1.0.0
 * =============================================================================
 */

// Re-export all schemas from their respective modules
// Each module contains schemas for a specific domain

// =============================================================================
// TEXT PROCESSING SCHEMAS
// =============================================================================
// Schemas related to text input, preprocessing, and cleaning

/**
 * RawTextInput: Unprocessed text from user or external source
 * This is the initial entry point for text data in the system
 */
export { RawTextInput, RawTextInputSchema } from './schemas/text.schema.js';

/**
 * PreprocessedText: Text after cleaning and normalization
 * This is the output from the preprocessing service
 */
export { PreprocessedText, PreprocessedTextSchema } from './schemas/text.schema.js';

/**
 * TextMetadata: Additional information about text data
 * Includes language, encoding, and processing history
 */
export { TextMetadata, TextMetadataSchema } from './schemas/text.schema.js';


// =============================================================================
// PREDICTION SCHEMAS
// =============================================================================
// Schemas related to model predictions and inference results

/**
 * PredictionResult: Single prediction from the model
 * Contains the predicted class, confidence, and supporting information
 */
export { PredictionResult, PredictionResultSchema } from './schemas/prediction.schema.js';

/**
 * BatchPredictionResult: Multiple predictions for batch processing
 * Optimized for processing multiple texts efficiently
 */
export { BatchPredictionResult, BatchPredictionResultSchema } from './schemas/prediction.schema.js';

/**
 * PredictionExplanation: Explainable AI output
 * Contains feature importance and attention weights for interpretability
 */
export { PredictionExplanation, PredictionExplanationSchema } from './schemas/prediction.schema.js';

/**
 * ConfidenceInterval: Statistical confidence bounds
 * Provides upper and lower bounds for predictions
 */
export { ConfidenceInterval, ConfidenceIntervalSchema } from './schemas/prediction.schema.js';


// =============================================================================
// TRAINING SCHEMAS
// =============================================================================
// Schemas related to model training and evaluation

/**
 * TrainingConfig: Configuration for model training
 * Contains hyperparameters, data paths, and training options
 */
export { TrainingConfig, TrainingConfigSchema } from './schemas/training.schema.js';

/**
 * TrainingMetrics: Metrics collected during training
 * Includes loss, accuracy, and custom metrics per epoch
 */
export { TrainingMetrics, TrainingMetricsSchema } from './schemas/training.schema.js';

/**
 * EvaluationResult: Model evaluation results
 * Contains precision, recall, F1, and other classification metrics
 */
export { EvaluationResult, EvaluationResultSchema } from './schemas/training.schema.js';

/**
 * ModelCheckpoint: Saved model state during training
 * Contains model weights, optimizer state, and metadata
 */
export { ModelCheckpoint, ModelCheckpointSchema } from './schemas/training.schema.js';


// =============================================================================
// FEATURE SCHEMAS
// =============================================================================
// Schemas related to feature extraction and embeddings

/**
 * TextFeatures: Extracted features from text
 * Contains embeddings, statistical features, and derived attributes
 */
export { TextFeatures, TextFeaturesSchema } from './schemas/features.schema.js';

/**
 * EmbeddingVector: Dense vector representation of text
 * Used for similarity search and as input to ML models
 */
export { EmbeddingVector, EmbeddingVectorSchema } from './schemas/features.schema.js';

/**
 * FeatureImportance: Importance scores for each feature
 * Used for model interpretability and feature selection
 */
export { FeatureImportance, FeatureImportanceSchema } from './schemas/features.schema.js';


// =============================================================================
// MODEL REGISTRY SCHEMAS
// =============================================================================
// Schemas related to model versioning and storage

/**
 * ModelMetadata: Information about a registered model
 * Includes version, author, creation date, and performance metrics
 */
export { ModelMetadata, ModelMetadataSchema } from './schemas/model.schema.js';

/**
 * ModelVersion: Specific version of a model
 * Tracks changes between model iterations
 */
export { ModelVersion, ModelVersionSchema } from './schemas/model.schema.js';

/**
 * ModelArtifact: Storage information for model files
 * Contains paths to model weights, config, and associated files
 */
export { ModelArtifact, ModelArtifactSchema } from './schemas/model.schema.js';


// =============================================================================
// SERVICE SCHEMAS
// =============================================================================
// Schemas related to service communication and health

/**
 * ServiceHealth: Health status of a service
 * Used for monitoring and load balancing
 */
export { ServiceHealth, ServiceHealthSchema } from './schemas/service.schema.js';

/**
 * ServiceStatus: Detailed status information
 * Includes uptime, memory usage, and request counts
 */
export { ServiceStatus, ServiceStatusSchema } from './schemas/service.schema.js';

/**
 * ApiError: Standardized error response
 * Ensures consistent error formatting across services
 */
export { ApiError, ApiErrorSchema } from './schemas/service.schema.js';

/**
 * PaginationParams: Pagination for list endpoints
 * Standardizes paginated API responses
 */
export { PaginationParams, PaginationParamsSchema } from './schemas/service.schema.js';


// =============================================================================
// TYPE EXPORTS
// =============================================================================
// Export TypeScript types for use in other packages

/**
 * ClassificationLabel: Valid classification labels
 * Enum of all possible bullying classifications
 */
export type { ClassificationLabel } from './types/prediction.types.js';

/**
 * ModelArchitecture: Available model architectures
 * Enum of supported deep learning architectures
 */
export type { ModelArchitecture } from './types/model.types.js';

/**
 * ServiceName: All available service names
 * Enum of all microservices in the system
 */
export type { ServiceName } from './types/service.types.js';


// =============================================================================
// UTILITY EXPORTS
// =============================================================================
// Export utility functions for working with schemas

/**
 * createZodSchema: Convert Pydantic schema to Zod
 * Enables validation in both Python and TypeScript
 */
export { createZodSchema } from './utils/schema-converter.util.js';

/**
 * validateSchema: Validate data against a schema
 * Provides consistent validation across services
 */
export { validateSchema } from './utils/schema-validator.util.js';

/**
 * serializeSchema: Convert schema to JSON
 * Enables schema sharing across service boundaries
 */
export { serializeSchema } from './utils/schema-serializer.util.js';


// =============================================================================
// RE-EXPORT FROM PYTHON
// =============================================================================
// These are documented in the Python pyproject.toml
// Python services will use these schemas for validation

/*
// Python equivalent imports (for reference):
from cyberbullying_nlp_core.schemas.text import (
    RawTextInput,
    PreprocessedText,
    TextMetadata
)
from cyberbullying_nlp_core.schemas.prediction import (
    PredictionResult,
    BatchPredictionResult,
    PredictionExplanation
)
from cyberbullying_nlp_core.schemas.training import (
    TrainingConfig,
    TrainingMetrics,
    EvaluationResult
)
from cyberbullying_nlp_core.schemas.features import (
    TextFeatures,
    EmbeddingVector
)
from cyberbullying_nlp_core.schemas.model import (
    ModelMetadata,
    ModelVersion,
    ModelArtifact
)
*/
